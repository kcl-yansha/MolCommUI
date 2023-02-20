###========================================================###
### MolCommUI --- v1.0                                     ###
### Date: 20/02/2023                                       ###
###========================================================###
# Disclaimer: Python3 software developed by the Yansha Group #
#             at King's College London (UK)                  #
# Link: https://www.yanshadeng.org                           #
#------------------------------------------------------------#
# Author(s):                                                 #
# - Vivien WALTER (walter.vivien@gmail.com)                  #
###========================================================###

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## DEFINE THE QUEUEING CLASS
##-/-/-/-/-/-/-/-/-/-/-/-/-/

class Queue:

    def __init__(self, maxsize=-1):
        self.queue = list()
        self.maxsize = maxsize

    ##-\-\-\-\-\-\-\-\
    ## ACCESS THE QUEUE
    ##-/-/-/-/-/-/-/-/

    # -------------------------
    # Enqueue the given command
    def enqueue(self, equipment_id, event_type, fn, *args, **kwargs):

        # Extract the arguments
        priority = kwargs.pop('priority', False)
        inQueue = kwargs.pop('inQueue', False)
        first = kwargs.pop('first', False)
        emptyQueue = kwargs.pop('emptyQueue', False)
        emptyEquipment = kwargs.pop('emptyEquipment', False)

        priority = kwargs.pop('priority', False)
        is_unique = kwargs.pop('is_unique', False)
        make_unique = kwargs.pop('make_unique', False)
        flush_equipment = kwargs.pop('flush_equipment', False)
        flush_queue = kwargs.pop('flush_queue', False)

        # Generate the event dictionary
        dict = {
        'type':event_type,
        'equipment_id':equipment_id,
        'function':fn,
        'arguments':args,
        'keywords':kwargs
        }

        # Initialise
        can_proceed = True

        ## Handle the content of the queue

        if flush_equipment: self.flush_equipment(event_type)

        if make_unique: self.flush_event(event_type)

        if flush_queue: self.flush()

        if is_unique and can_proceed: can_proceed = not self.isQueued(event_type, first=first)

        ## Add to the top of the queue if needed
        if can_proceed:
            if priority: self.queue.append( dict )
            else: self.queue.insert(0, dict )

    # -------------------------
    # Enqueue the given command
    def _old_enqueue(self, equipment_id, event_type, fn, *args, **kwargs):

        # Extract the arguments
        priority = kwargs.pop('priority', False)
        inQueue = kwargs.pop('inQueue', False)
        first = kwargs.pop('first', False)
        emptyQueue = kwargs.pop('emptyQueue', False)
        emptyEquipment = kwargs.pop('emptyEquipment', False)

        # Generate the event dictionary
        dict = {
        'type':event_type,
        'equipment_id':equipment_id,
        'function':fn,
        'arguments':args,
        'keywords':kwargs
        }

        _proceed = True

        # Check if full
        if self.maxsize > 0:
            _proceed = self.getCount() < self.maxsize

        # Empty queue on call
        if emptyQueue:
            self.flush()
        if emptyEquipment:
            self.flush(event_type)

        # Check if unique
        if inQueue and _proceed:
            _proceed = not self.isQueued(event_type, first=first)

        # Proceed if allowed
        if _proceed:

            # Add to the top of the queue if needed
            if priority:
                self.queue.append( dict )

            else:
                self.queue.insert(0, dict )

    # ---------------------------------
    # Get the next event from the queue
    def dequeue(self):

        # Check if the queue is not empty
        if len(self.queue)> 0:

            # Extract the dictionary
            dict = self.queue.pop()
            fn, args, kwargs = dict['function'], dict['arguments'], dict['keywords']

            # Get the verbose state
            verbose = kwargs.get('verbose', False)

            # Execute the command in the queue
            return True, dict['equipment_id'], fn(*args, **kwargs), verbose

        else:
            return False, None, None, False

    ##-\-\-\-\-\-\-\-\
    ## QUEUE MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Remove all the elements currently queued
    def flush(self, event_type=None):
        self.queue = list()

    # ----------------------------------------
    # Remove all the elements currently queued
    def flush_equipment(self, event_type):
        flag = event_type.replace(event_type.split('-')[-1], '')
        self.queue = [x for x in self.queue if flag not in x]

    # --------------------------------
    # Remove all instance of the event
    def flush_event(self, event_type):
        self.queue = [x for x in self.queue if x != event_type]

    # ---------------------------------------
    # Check if the event type is in the queue
    def isQueued(self, event_type, first=False):

        # Only check the first element
        if first:
            first_type = self.queue[-1]['type']

            return first_type == event_type

        # Check all elements
        else:
            all_types = [x['type'] for x in self.queue]

            return event_type in all_types

    ### OLD

    # --------------------------------------------------
    # Return the number of events currently in the queue
    def getCount(self):
        return len( self.queue )
