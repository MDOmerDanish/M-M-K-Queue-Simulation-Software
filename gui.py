import tkinter as tk

from exp import*
from exp3 import*
from exp4 import*
from exp3_for_graph_plot import*
from exp4_for_graph_plot import*
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def hello(*args):
	
	print(args[0])
	print(args[1])
	print(args[2])
	print(args[3])

	mu=float(args[0])
	lambd=float(args[1])
	k=int(args[2])
	no_of_queue=int(args[3])
	result=[]
	if k==no_of_queue and k==1:
	   print('exp 1')
	   result=experiment1(mu,lambd,k)
	elif k>1 and no_of_queue==1:
	   print('exp 3')
	   result=experiment3(mu,lambd,k,no_of_queue)	
	elif k==no_of_queue and k>1:
	   print('exp 4')
	   result=experiment4(mu,lambd,k,no_of_queue)   



	l1=Label(args[4],text=str(result[0]),bg='cyan',font="comicsansms 20 bold",borderwidth=3, relief="solid",padx=10,pady=10)
	l1.grid(row=0,column=3,pady=20)
	
	l1=Label(args[4],text=str(result[1]),bg='cyan',font="comicsansms 20 bold",borderwidth=3, relief="solid",padx=10,pady=10)
	l1.grid(row=3,column=3,pady=20)

	l1=Label(args[4],text=str(result[2]),bg='cyan',font="comicsansms 20 bold",borderwidth=3, relief="solid",padx=10,pady=10)
	l1.grid(row=2,column=3,pady=20)





def plot_graph(*args):
	

	print(args[0])
	print(args[1])
	print(args[2])


	lambd=float(args[0])
	mu=float(args[1])
	k=int(args[2])
	result=[]
	print(args[3])
	if args[3]=='Single queue':	
	   result=experiment3_for_graph_plot(lambd,mu,k)
	   print('plotting exp 3')
	if args[3]=='Queue_no = Server_no':
	   result=experiment4_for_graph_plot(lambd,mu,k)
	   print('plotting exp 4')

	ratios = [u  for u in range(1,k+1)]
	figure = Figure(figsize=(14,3), dpi=100)

	plot = figure.add_subplot(1,3,1)
	plot.plot(ratios,result[0])
	plot.set_title('No of Server Vs. avglength')
	plot.set(xlabel='', ylabel='avglength')
	canvas = FigureCanvasTkAgg(figure,args[4])
	canvas.get_tk_widget().grid(row=0, column=0)


	plot = figure.add_subplot(1,3,2)
	plot.plot(ratios,result[1])
	plot.set_title('No of Server Vs. avgdelay')
	plot.set(xlabel='', ylabel='avgdelay')
	canvas = FigureCanvasTkAgg(figure,args[4])
	canvas.get_tk_widget().grid(row=0, column=0)
	




	plot = figure.add_subplot(1,3,3)
	plot.plot(ratios,result[2])
	plot.set_title('No of Server Vs. Utility')
	plot.set(xlabel='', ylabel='Utility')
	canvas = FigureCanvasTkAgg(figure,args[4])
	canvas.get_tk_widget().grid(row=0, column=0)



def compare_single_queue_systems(*args):


	window2=Tk()
	window2.geometry('1500x600')
	window2.minsize(500,400)
	window2.maxsize(1250,800)


	variable = StringVar(window2)
	variable.set("Simulation option ") # default value
	w = OptionMenu(window2, variable, "Single queue", "Queue_no = Server_no")
#	w.config(font=('calibri',(20)),width=17,bg='orange',borderwidth=3)
	w.config(font='comicsansms 18 bold',width=17,bg='orange',borderwidth=3)
	w.grid(row=1,column=0,rowspan=4,padx=2,sticky='w')
	print(variable.get())
	
	l1=Label(window2,text='Arrival Rate',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=4,column=0,padx=350,pady=20,sticky='w')

	l1=Label(window2,text='Service Rate',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=5,column=0,padx=350,pady=20,sticky='w')

	l1=Label(window2,text='No of Server',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=6,column=0,padx=350,pady=20,sticky='w')



	arrival_text=StringVar()
	e1=Entry(window2,textvariable=arrival_text,font="comicsansms 20 bold",width=10,borderwidth=5)
	e1.grid(row=4,column=0,pady=20)
	#e1.place(x=200,y=150)
	service_text=StringVar()
	e2=Entry(window2,textvariable=service_text,font="comicsansms 20 bold",width=10,borderwidth=5)
	e2.grid(row=5,column=0,pady=20)


	server_text=StringVar()
	e3=Entry(window2,textvariable=server_text,font="comicsansms 20 bold",width=10,borderwidth=5)
	e3.grid(row=6,column=0,pady=20)


	# getting screen's height in pixels 
	height = window2.winfo_screenmmheight()   
	# getting screen's width in pixels 
	width = window2.winfo_screenmmwidth() 

	

	figure = Figure(figsize=(14,3.3), dpi=100)

	plot = figure.add_subplot(1,3,1)	
	#box = plot.get_position()
	#plot.set_position([box.x0, box.y0, box.width * 1 , box.height * 1])
	plot.set_title('No of Server Vs. avglength')
	plot.set(xlabel='', ylabel='avglength')
	canvas = FigureCanvasTkAgg(figure,window2)
	canvas.get_tk_widget().grid(row=0, column=0)

	
	plot = figure.add_subplot(1,3,2)
	plot.set_title('No of Server Vs. avgdelay')
	plot.set(xlabel='', ylabel='avgdelay')
	canvas = FigureCanvasTkAgg(figure,window2)
	canvas.get_tk_widget().grid(row=0, column=0)
	
	plot = figure.add_subplot(1,3,3)
	plot.set_title('No of Server Vs. Utility')
	plot.set(xlabel='', ylabel='Utility')
	canvas = FigureCanvasTkAgg(figure,window2)
	canvas.get_tk_widget().grid(row=0, column=0)


	
	
	b1 = Button(window2, text='Simulate',height=2,width=10,command=lambda :plot_graph(e1.get(),e2.get(),e3.get(),variable.get(),window2),font="comicsansms 20 bold",activebackground='green2') 
	b1.grid(row=7,column=0,padx=350,pady=20,sticky='w')

	
	b2 = Button(window2, text='Exit',height=2,width=10,command=window2.quit,font="comicsansms 20 bold",activebackground='red') 
	b2.grid(row=7,column=0)



	b3 = Button(window2, text='Back to home',height=2,width=10,command =window2.destroy,font="comicsansms 20 bold",activebackground='green2') 
	b3.grid(row=7,column=0,padx=60,sticky='w')
	#b3.grid(row=5,column=2,pady=80)
	b3.bind('<Button-1>')




def gui(*args):
	

	window=Tk()
	window.geometry('1500x600')
	window.minsize(500,400)
	window.maxsize(1250,800)

	l1=Label(window,text='Arrival Rate',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=0,column=0,pady=20)

	l1=Label(window,text='No of server',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=3,column=0,pady=20)

	l1=Label(window,text='Service Rate',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=2,column=0,pady=20)

	l1=Label(window,text='No of queue',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=4,column=0,pady=20)


	l1=Label(window,text='Average queue length:',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=0,column=2,padx=80,pady=20)
	
	l1=Label(window,text='Average queue delay:',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=3,column=2,pady=20)

	l1=Label(window,text='Average server utility:',bg='orange',font="comicsansms 20 bold",borderwidth=3, relief="solid")
	l1.grid(row=2,column=2,pady=20)




	arrival_text=StringVar()
	e1=Entry(window,textvariable=arrival_text,font="comicsansms 20 bold",width=8,borderwidth=5)
	e1.grid(row=0,column=1,pady=20)

	service_text=StringVar()
	e2=Entry(window,textvariable=service_text,font="comicsansms 20 bold",width=8,borderwidth=5)
	e2.grid(row=2,column=1,pady=20)


	server_text=StringVar()
	e3=Entry(window,textvariable=server_text,font="comicsansms 20 bold",width=8,borderwidth=5)
	e3.grid(row=3,column=1,pady=20)

	queue_text=StringVar()
	e4=Entry(window,textvariable=queue_text,font="comicsansms 20 bold",width=8,borderwidth=5)
	e4.grid(row=4,column=1,pady=20)


	b1 = Button(window, text='Simulate',height=2,width=10,command =lambda :hello(e1.get(),e2.get(),e3.get(),e4.get(),window),font="comicsansms 20 bold",activebackground='green2') 
	b1.grid(row=8,column=1,pady=80)
	b1.bind('<Button-1>,<Return>')
	#b1.bind('<Return>')



	b3 = Button(window, text='Back to home',height=2,width=10,command =window.destroy,font="comicsansms 20 bold",activebackground='green2') 
	b3.grid(row=8,column=2)
	#b3.grid(row=5,column=2,pady=80)
	b3.bind('<Button-1>')


	b2 = Button(window, text='Exit',height=2,width=10,command=window.quit,font="comicsansms 20 bold",activebackground='red') 
	b2.grid(row=8,column=3,pady=80)
	#b2.grid(row=12,column=1)

	window.mainloop()



def homepage():
	

	window=Tk()
	window.geometry('1500x600')
	window.minsize(500,400)
	window.maxsize(1250,800)

	l1=Label(window,text='WELCOME TO SERVER QUEUE SYSTEM SIMULATION',bg='cyan',font="comicsansms 30 bold",borderwidth=3, relief="solid")
	l1.grid(row=0,column=0,columnspan=15,padx=100,pady=50)




	b1 = Button(window, text='Simulation by plotting graph',height=2,width=30,command =lambda :compare_single_queue_systems(window),font="comicsansms 20 bold",activebackground='green2') 
	b1.grid(row=4,column=2,padx=350,pady=30)
	b1.bind('<Button-1>,<Return>')
	#b1.bind('<Return>')


	b2 = Button(window, text='Simulation by single point',height=2,width=30,command=lambda :gui(window),font="comicsansms 20 bold",activebackground='green2') 
	b2.grid(row=5,column=2,pady=30)




	b3 = Button(window, text='Exit',height=2,width=10,command=window.quit,font="comicsansms 20 bold",activebackground='red') 
	b3.grid(row=6,column=2,padx=400,pady=30)


	window.mainloop()


def main():
    homepage()


if __name__ == "__main__":
    main()
