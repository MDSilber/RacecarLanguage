from Tkinter import *

class EditorClass(object):

    UPDATE_PERIOD = 100 #ms

    editors = []
    updateId = None

    def __init__(self, text_width=16,text_height=20):
        
        self.__class__.editors.append(self)

        self.lineNumbers = ''

        # A frame to hold the three components of the widget.
        self.frame = Frame(master, bd=2, relief=SUNKEN)

        # The widgets vertical scrollbar
        self.vScrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.vScrollbar.pack(fill='y', side=RIGHT)

        # The Text widget holding the line numbers.
        self.lnText = Text(self.frame,
                width = 4,
                padx = 4,
                highlightthickness = 0,
                takefocus = 0,
                bd = 0,
                background = 'lightgrey',
                foreground = 'magenta',
                state='disabled',
								height=text_height
        )
        self.lnText.pack(side=LEFT, fill='y')

        # The Main Text Widget
        self.text = Text(self.frame,
                width=text_width,
								height=text_height,
                bd=0,
                padx = 4,
                undo=True,
                background = 'white'
        )
        self.text.pack(side=LEFT, fill=BOTH, expand=1)

        self.text.config(yscrollcommand=self.vScrollbar.set)
        self.vScrollbar.config(command=self.text.yview)

        if self.__class__.updateId is None:
            self.updateAllLineNumbers()
   
    def getLineNumbers(self):
        
        x = 0
        line = '0'
        col= ''
        ln = ''
        
        # assume each line is at least 6 pixels high
        step = 6
        
        nl = '\n'
        lineMask = '    %s\n'
        indexMask = '@0,%d'
        
        for i in range(0, self.text.winfo_height(), step):
            
            ll, cc = self.text.index( indexMask % i).split('.')

            if line == ll:
                if col != cc:
                    col = cc
                    ln += nl
            else:
                line, col = ll, cc
                ln += (lineMask % line)[-5:]

        return ln

    def updateLineNumbers(self):

        tt = self.lnText
        ln = self.getLineNumbers()
        if self.lineNumbers != ln:
            self.lineNumbers = ln
            tt.config(state='normal')
            tt.delete('1.0', END)
            tt.insert('1.0', self.lineNumbers)
            tt.config(state='disabled')
        
    @classmethod
    def updateAllLineNumbers(cls):

        if len(cls.editors) < 1:
            cls.updateId = None
            return
        
        for ed in cls.editors:
            ed.updateLineNumbers()
        
        cls.updateId = ed.text.after(
            cls.UPDATE_PERIOD,
            cls.updateAllLineNumbers)
