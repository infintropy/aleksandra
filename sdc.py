



from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *




class Sidecar(QWidget):
    def __init__(self):
        super(Sidecar, self).__init__()

        self.fontSize = 11

        self.master_layout = QVBoxLayout()
        self.setLayout( self.master_layout )





        """
        
        Trigger: list of commands to check for associated commands. 

        
        NodeFocus - [Blur]
        NodeSelection - [Blur, Merge, NamedGroup]
        
        
        
        
        Trigger List |  
        
        """












        self.scriptEditorScript = KnobScripterEditorWidget(self)
        self.scriptEditorScript.setMinimumHeight(100)
        self.scriptEditorScript.setStyleSheet('background:#282828;color:#EEE;') # Main Colors
        KSScriptEditorHighlighter(self.scriptEditorScript.document())
        self.scriptEditorFont = QFont()
        self.scriptEditorFont.setFamily("Courier")
        self.scriptEditorFont.setStyleHint(QFont.Monospace)
        self.scriptEditorFont.setFixedPitch(True)
        self.scriptEditorFont.setPointSize(self.fontSize)
        self.scriptEditorScript.setFont(self.scriptEditorFont)
        self.scriptEditorScript.setTabStopWidth(4 * QFontMetrics(self.scriptEditorFont).width(' '))

        self.master_layout.addWidget(self.scriptEditorScript)




#------------------------------------------------------------------------------------------------------
# Script Editor Widget
# Wouter Gilsing built an incredibly useful python script editor for his Hotbox Manager, so I had it
# really easy for this part! I made it a bit simpler, leaving just the part non associated to his tool
# and tweaking the style a bit to be compatible with font size changing and stuff.
# I think this bit of code has the potential to get used in many nuke tools.
# All credit to him: http://www.woutergilsing.com/
# Originally used on W_Hotbox v1.5: http://www.nukepedia.com/python/ui/w_hotbox
#------------------------------------------------------------------------------------------------------

class KnobScripterEditorWidget(QPlainTextEdit):

    # pyqtSignal that will be emitted when the user has changed the text
    userChangedEvent = pyqtSignal()

    def __init__(self, knobScripter):
        super(KnobScripterEditorWidget, self).__init__()
        self.knobScripter = knobScripter

        # Setup line numbers
        self.lineNumberArea = KSLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth()

        # Highlight line
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

    #--------------------------------------------------------------------------------------------------
    # Line Numbers (extract from original comment by Wouter Gilsing)
    # While researching the implementation of line number, I had a look at Nuke's Blinkscript node. [..]
    # thefoundry.co.uk/products/nuke/developers/100/pythonreference/nukescripts.blinkscripteditor-pysrc.html
    # I stripped and modified the useful bits of the line number related parts of the code [..]
    # Credits to theFoundry for writing the blinkscripteditor, best example code I could wish for.
    #--------------------------------------------------------------------------------------------------

    def lineNumberAreaWidth(self):
        digits = 1
        maxNum = max(1, self.blockCount())
        while (maxNum >= 10):
            maxNum /= 10
            digits += 1

        space = 7 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):

        if (dy):
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if (rect.contains(self.viewport().rect())):
            self.updateLineNumberAreaWidth()

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):

        if self.isReadOnly():
            return

        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(36, 36, 36)) # Number bg


        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int( self.blockBoundingGeometry(block).translated(self.contentOffset()).top() )
        bottom = top + int( self.blockBoundingRect(block).height() )
        currentLine = self.document().findBlock(self.textCursor().position()).blockNumber()

        painter.setPen( self.palette().color(QPalette.Text) )

        painterFont = QFont()
        painterFont.setFamily("Courier")
        painterFont.setStyleHint(QFont.Monospace)
        painterFont.setFixedPitch(True)
        painterFont.setPointSize(self.knobScripter.fontSize)
        painter.setFont(self.knobScripter.scriptEditorFont)

        while (block.isValid() and top <= event.rect().bottom()):

            textColor = QColor(110, 110, 110) # Numbers

            if blockNumber == currentLine and self.hasFocus():
                textColor = QColor(255, 170, 0) # Number highlighted

            painter.setPen(textColor)

            number = "%s" % str(blockNumber + 1)
            painter.drawText(-3, top, self.lineNumberArea.width(), self.fontMetrics().height(), Qt.AlignRight, number)

            # Move to the next block
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    #--------------------------------------------------------------------------------------------------
    # Auto indent
    #--------------------------------------------------------------------------------------------------

    def keyPressEvent(self, event):
        '''
        Custom actions for specific keystrokes
        '''

        #if Tab convert to Space
        if event.key() == 16777217:
            self.indentation('indent')

        #if Shift+Tab remove indent
        elif event.key() == 16777218:

            self.indentation('unindent')

        #if BackSpace try to snap to previous indent level
        elif event.key() == 16777219:
            if not self.unindentBackspace():
                QPlainTextEdit.keyPressEvent(self, event)

        #if enter or return, match indent level
        elif event.key() in [16777220 ,16777221]:
            #QPlainTextEdit.keyPressEvent(self, event)
            self.indentNewLine()
        else:
            QPlainTextEdit.keyPressEvent(self, event)

    #--------------------------------------------------------------------------------------------------

    def getCursorInfo(self):

        self.cursor = self.textCursor()

        self.firstChar =  self.cursor.selectionStart()
        self.lastChar =  self.cursor.selectionEnd()

        self.noSelection = False
        if self.firstChar == self.lastChar:
            self.noSelection = True

        self.originalPosition = self.cursor.position()
        self.cursorBlockPos = self.cursor.positionInBlock()
    #--------------------------------------------------------------------------------------------------

    def unindentBackspace(self):
        '''
        #snap to previous indent level
        '''
        self.getCursorInfo()

        if not self.noSelection or self.cursorBlockPos == 0:
            return False

        #check text in front of cursor
        textInFront = self.document().findBlock(self.firstChar).text()[:self.cursorBlockPos]

        #check whether solely spaces
        if textInFront != ' '*self.cursorBlockPos:
            return False

        #snap to previous indent level
        spaces = len(textInFront)
        for space in range(spaces - ((spaces -1) /4) * 4 -1):
            self.cursor.deletePreviousChar()

    def indentNewLine(self):

        #in case selection covers multiple line, make it one line first
        self.insertPlainText('')

        self.getCursorInfo()

        #check how many spaces after cursor
        text = self.document().findBlock(self.firstChar).text()

        textInFront = text[:self.cursorBlockPos]

        if len(textInFront) == 0:
            self.insertPlainText('\n')
            return

        indentLevel = 0
        for i in textInFront:
            if i == ' ':
                indentLevel += 1
            else:
                break

        indentLevel /= 4

        #find out whether textInFront's last character was a ':'
        #if that's the case add another indent.
        #ignore any spaces at the end, however also
        #make sure textInFront is not just an indent
        if textInFront.count(' ') != len(textInFront):
            while textInFront[-1] == ' ':
                textInFront = textInFront[:-1]

        if textInFront[-1] == ':':
            indentLevel += 1

        #new line
        self.insertPlainText('\n')
        #match indent
        self.insertPlainText(' '*(4*int(indentLevel)))

    def indentation(self, mode):

        self.getCursorInfo()

        #if nothing is selected and mode is set to indent, simply insert as many
        #space as needed to reach the next indentation level.
        if self.noSelection and mode == 'indent':

            remainingSpaces = 4 - (self.cursorBlockPos%4)
            self.insertPlainText(' '*remainingSpaces)
            return

        selectedBlocks = self.findBlocks(self.firstChar, self.lastChar)
        beforeBlocks = self.findBlocks(last = self.firstChar -1, exclude = selectedBlocks)
        afterBlocks = self.findBlocks(first = self.lastChar + 1, exclude = selectedBlocks)

        beforeBlocksText = self.blocks2list(beforeBlocks)
        selectedBlocksText = self.blocks2list(selectedBlocks, mode)
        afterBlocksText = self.blocks2list(afterBlocks)

        combinedText = '\n'.join(beforeBlocksText + selectedBlocksText + afterBlocksText)

        #make sure the line count stays the same
        originalBlockCount = len(self.toPlainText().split('\n'))
        combinedText = '\n'.join(combinedText.split('\n')[:originalBlockCount])

        self.clear()
        self.setPlainText(combinedText)

        if self.noSelection:
            self.cursor.setPosition(self.lastChar)

        #check whether the the orignal selection was from top to bottom or vice versa
        else:
            if self.originalPosition == self.firstChar:
                first = self.lastChar
                last = self.firstChar
                firstBlockSnap = QTextCursor.EndOfBlock
                lastBlockSnap = QTextCursor.StartOfBlock
            else:
                first = self.firstChar
                last = self.lastChar
                firstBlockSnap = QTextCursor.StartOfBlock
                lastBlockSnap = QTextCursor.EndOfBlock

            self.cursor.setPosition(first)
            self.cursor.movePosition(firstBlockSnap,QTextCursor.MoveAnchor)
            self.cursor.setPosition(last,QTextCursor.KeepAnchor)
            self.cursor.movePosition(lastBlockSnap,QTextCursor.KeepAnchor)

        self.setTextCursor(self.cursor)

    def findBlocks(self, first = 0, last = None, exclude = []):
        blocks = []
        if last == None:
            last = self.document().characterCount()
        for pos in range(first,last+1):
            block = self.document().findBlock(pos)
            if block not in blocks and block not in exclude:
                blocks.append(block)
        return blocks

    def blocks2list(self, blocks, mode = None):
        text = []
        for block in blocks:
            blockText = block.text()
            if mode == 'unindent':
                if blockText.startswith(' '*4):
                    blockText = blockText[4:]
                    self.lastChar -= 4
                elif blockText.startswith('\t'):
                    blockText = blockText[1:]
                    self.lastChar -= 1

            elif mode == 'indent':
                blockText = ' '*4 + blockText
                self.lastChar += 4

            text.append(blockText)

        return text

    #--------------------------------------------------------------------------------------------------
    #current line hightlighting
    #--------------------------------------------------------------------------------------------------

    def highlightCurrentLine(self):
        '''
        Highlight currently selected line
        '''
        extraSelections = []

        selection = QTextEdit.ExtraSelection()

        lineColor = QColor(62, 62, 62, 255)

        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        extraSelections.append(selection)

        self.setExtraSelections(extraSelections)



################################################################################################

class KSLineNumberArea(QWidget):
    def __init__(self, scriptEditor):
        super(KSLineNumberArea, self).__init__(scriptEditor)

        self.scriptEditor = scriptEditor
        self.setStyleSheet("text-align: center;")

    def paintEvent(self, event):
        self.scriptEditor.lineNumberAreaPaintEvent(event)
        return

class KSScriptEditorHighlighter(QSyntaxHighlighter):
    '''
    Modified, simplified version of some code found I found when researching:
    wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
    They did an awesome job, so credits to them. I only needed to make some
    modifications to make it fit my needs.
    '''

    def __init__(self, document):

        super(KSScriptEditorHighlighter, self).__init__(document)

        self.styles = {
            'keyword': self.format([238,117,181],'bold'),
            'string': self.format([242, 136, 135]),
            'comment': self.format([143, 221, 144 ]),
            'numbers': self.format([174, 129, 255])
            }

        self.keywords = [
            'and', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in',
            'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'while', 'yield'
            ]

        self.operatorKeywords = [
            '=','==', '!=', '<', '<=', '>', '>=',
            '\+', '-', '\*', '/', '//', '\%', '\*\*',
            '\+=', '-=', '\*=', '/=', '\%=',
            '\^', '\|', '\&', '\~', '>>', '<<'
            ]

        self.numbers = ['True','False','None']

        self.tri_single = (QRegExp("'''"), 1, self.styles['comment'])
        self.tri_double = (QRegExp('"""'), 2, self.styles['comment'])

        #rules
        rules = []

        rules += [(r'\b%s\b' % i, 0, self.styles['keyword']) for i in self.keywords]
        rules += [(i, 0, self.styles['keyword']) for i in self.operatorKeywords]
        rules += [(r'\b%s\b' % i, 0, self.styles['numbers']) for i in self.numbers]

        rules += [

            # integers
            (r'\b[0-9]+\b', 0, self.styles['numbers']),
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles['string']),
            # From '#' until a newline
            (r'#[^\n]*', 0, self.styles['comment']),
            ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]

    def format(self,rgb, style=''):
        '''
        Return a QTextCharFormat with the given attributes.
        '''

        color = QColor(*rgb)
        textFormat = QTextCharFormat()
        textFormat.setForeground(color)

        if 'bold' in style:
            textFormat.setFontWeight(QFont.Bold)
        if 'italic' in style:
            textFormat.setFontItalic(True)

        return textFormat

    def highlightBlock(self, text):
        '''
        Apply syntax highlighting to the given block of text.
        '''
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        '''
        Check whether highlighting reuires multiple lines.
        '''
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False