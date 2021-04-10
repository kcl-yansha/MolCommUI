// -----------------------------
// MATHS.INO
//
// Include here the maths functions used in the script
//------------------------------

//==========
// VARIABLES
//==========

//=================
// PUBLIC FUNCTIONS
//=================

// -------------------------------------------------------
// Function to get the sum of all the elements on an array
int array_sum(int * array, int len) {
  
  int arraySum;
  arraySum = 0;
  
  for(int index = 0; index < len; index++)
  { arraySum += array[index]; }
  
  return arraySum;
}
