import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## PROXY STYLE FOR BUTTON WITH ICON
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
class ProxyStyle(qtw.QProxyStyle):

    # Draw the control
    def drawControl(self, element, option, painter, widget=None):

        # Check the source of the icon
        if element == qtw.QStyle.CE_PushButtonLabel:
            icon = qtg.QIcon(option.icon)
            option.icon = qtg.QIcon()

        super(ProxyStyle, self).drawControl(element, option, painter, widget)

        if element == qtw.QStyle.CE_PushButtonLabel:

            if not icon.isNull():
                iconSpacing = 4

                mode = (
                    qtg.QIcon.Normal
                    if option.state & qtw.QStyle.State_Enabled
                    else qtg.QIcon.Disabled
                )

                if (
                    mode == qtg.QIcon.Normal
                    and option.state & qtw.QStyle.State_HasFocus
                ):
                    mode = qtg.QIcon.Active
                state = qtg.QIcon.Off

                if option.state & qtw.QStyle.State_On:
                    state = qtg.QIcon.On

                window = widget.window().windowHandle() if widget is not None else None

                pixmap = icon.pixmap(window, option.iconSize, mode, state)
                pixmapWidth = pixmap.width() / pixmap.devicePixelRatio()
                pixmapHeight = pixmap.height() / pixmap.devicePixelRatio()

                iconRect = qtc.QRect(
                    qtc.QPoint(), qtc.QSize(pixmapWidth, pixmapHeight)
                )

                iconRect.moveCenter(option.rect.center())
                iconRect.moveLeft(option.rect.left() + iconSpacing)
                iconRect = self.visualRect(option.direction, option.rect, iconRect)
                iconRect.translate(
                    self.proxy().pixelMetric(
                        qtw.QStyle.PM_ButtonShiftHorizontal, option, widget
                    ),
                    self.proxy().pixelMetric(
                        qtw.QStyle.PM_ButtonShiftVertical, option, widget
                    ),
                )

                painter.drawPixmap(iconRect, pixmap)
