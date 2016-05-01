from Tkinter import *
import tkFont
from am_receive import am_receive

class GUI:
    def __init__(self, master):
        frame = Frame(master)
        self.f = frame
        frame.grid(row=7,column=4)
        self.flag1 = 0
        self.flag2 = 0
        self.flag3 = 0
        self.flag4 = 0
        self.flag5 = 0

        self.custom_font = tkFont.Font(font='bold', family='Helvetica', size=40)

        main_label = Label(frame, text='Winter Training Project', pady=20, font=self.custom_font)
        main_label.grid(row=0,column=1)

        label1 = Label(frame, text='Input File:', padx=20, pady=20)
        label1.grid(row=1, column=0)

        self.entryText1 = StringVar()
        self.entry1 = Entry(frame, textvariable=self.entryText1)
        self.entry1.grid(row=1, column=1)

        self.ques_btn1 = Button(frame, text='Browse', padx=10, pady=10, command=self.browsecsv)
        self.ques_btn1.grid(row=1, column=2)

        label2 = Label(frame, text='Frequency Range (min,max)', padx=30, pady=20)
        label2.grid(row=2, column=0)

        self.entry2 = Entry(frame)
        self.entry2.grid(row=2, column=1)

        self.ques_btn2 = Button(frame, text='?', padx=10, pady=10, command=self.showfreqlabel)
        self.ques_btn2.grid(row=2, column=2)

        label3 = Label(frame, text='Volume Range (min,max)', padx=30, pady=20)
        label3.grid(row=3, column=0)

        self.entry3 = Entry(frame)
        self.entry3.grid(row=3, column=1)

        self.ques_btn3 = Button(frame, text='?', padx=10, pady=10, command=self.showvollabel)
        self.ques_btn3.grid(row=3, column=2)

        label4 = Label(frame, text='Sample Rate', padx=30, pady=20)
        label4.grid(row=4, column=0)

        self.entry4 = Entry(frame)
        self.entry4.grid(row=4, column=1)

        self.ques_btn4 = Button(frame, text='?', padx=10, pady=10, command=self.showsampratelabel)
        self.ques_btn4.grid(row=4, column=2)

        label5 = Label(frame, text='Re-samp Factor', padx=30, pady=20)
        label5.grid(row=5, column=0)

        self.entry5 = Entry(frame)
        self.entry5.grid(row=5, column=1)

        self.ques_btn5 = Button(frame, text='?', padx=10, pady=10, command=self.showresampratelabel)
        self.ques_btn5.grid(row=5, column=2)

        label6 = Label(frame, text='Cut-off Frequency', padx=30, pady=20)
        label6.grid(row=6, column=0)

        self.entry6 = Entry(frame)
        self.entry6.grid(row=6, column=1)

        self.ques_btn6 = Button(frame, text='?', padx=10, pady=10, command=self.showcutofflabel)
        self.ques_btn6.grid(row=6, column=2)

        self.runbutton = Button(frame, text='Run', fg='red', padx=70, pady=20, command=self.runGNU)
        self.runbutton.grid(row=7,column=3)

    def browsecsv(self):
        from tkFileDialog import askopenfilename
        Tk().withdraw()
        filepath = askopenfilename()
        self.entryText1.set(filepath)

    def showfreqlabel(self):
        if (self.flag1 == 1):
            self.flag1 = 0
            self.label_freq.grid_remove()
        else:
            self.flag1 = 1
            self.label_freq = Label(self.f, text='Range of frequency in Hz')
            self.label_freq.grid(row=2, column=3)

    def showvollabel(self):
        if (self.flag2 == 1):
            self.flag2 = 0
            self.label_volume.grid_remove()
        else:
            self.flag2 = 1
            self.label_volume = Label(self.f, text='Range of magnitude\nreceived by speakers')
            self.label_volume.grid(row=3, column=3)

    def showsampratelabel(self):
        if(self.flag3==1):
            self.flag3=0
            self.label_samprate.grid_remove()
        else:
            self.flag3=1
            self.label_samprate = Label(self.f, text='Rate at which i/p signals\nare sampled')
            self.label_samprate.grid(row=4, column=3)

    def showresampratelabel(self):
        if(self.flag4==1):
            self.flag4=0
            self.label_resamp.grid_remove()
        else:
            self.flag4 = 1
            self.label_resamp = Label(self.f, text='Factor by which sample rate is to\n be divided')
            self.label_resamp.grid(row=5, column=3)

    def showcutofflabel(self):
        if(self.flag5==1):
            self.flag5=0
            self.label_cutofffreq.grid_remove()
        else:
            self.flag5 = 1
            self.label_cutofffreq = Label(self.f, text='Cutoff-frequency of the\nLow-pass filter')
            self.label_cutofffreq.grid(row=6, column=3)

    def runGNU(self):
        #input_file,min_frequency,max_frequency,min_volume,max_volume,sample_rate,resamp_rate,cutoff_frequency

        if self.entry1.get() == '' or self.entry2.get() == '' or self.entry3.get() == '' or self.entry3.get() == '' or self.entry4.get() == '' or self.entry5.get() == '' or self.entry6.get() == '':
            error_label = Label(self.f, text='Kindly enter all values.', fg='red')
            error_label.grid(row=7, column='0')
            return
        try:
            input_file = self.entry1.get()
            if (self.entry2.get().split(',').__len__() == 2):
                min_frequency = int(self.entry2.get().split(',')[0])
                max_frequency = int(self.entry2.get().split(',')[1])
            else:
                error_label = Label(self.f, text='Error! Enter range correctly.', fg='red')
                error_label.grid(row=7, column='0')
                return
            if(self.entry3.get().split(',').__len__()==2):
                min_volume = int(self.entry3.get().split(',')[0])
                max_volume = int(self.entry3.get().split(',')[1])
            else:
                error_label = Label(self.f, text='Error! Enter range correctly.', fg='red')
                error_label.grid(row=7, column='0')
                return
            if(min_volume>max_volume or min_frequency>max_frequency):
                error_label = Label(self.f, text='Error! Enter range correctly.', fg='red')
                error_label.grid(row=7, column='0')
                return
            sample_rate = int(self.entry4.get())
            resamp_rate = int(self.entry5.get())
            cutoff_frequency = int(self.entry6.get())
            print input_file,min_frequency,max_frequency,min_volume,max_volume,sample_rate,resamp_rate,cutoff_frequency
            error_label = Label(self.f, text='Running...', fg='green')
            error_label.grid(row=7, column='0')

            tb = am_receive(input_file,min_frequency,max_frequency,min_volume,max_volume,sample_rate,resamp_rate,cutoff_frequency)
            tb.Start(True)
            tb.Wait()

        except ValueError:
            error_label = Label(self.f, text = 'Error! All values must be integer', fg='red')
            error_label.grid(row=7, column='0')
            return
        except IndexError:
            error_label = Label(self.f, text='Error! Enter range', fg='red')
            error_label.grid(row=7, column='0')
            return


root = Tk()
root.geometry("700x500+100+150")
root.wm_title('Radio Receiver')
a = GUI(root)
root.mainloop()