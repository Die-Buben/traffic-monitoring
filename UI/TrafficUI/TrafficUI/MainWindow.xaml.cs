using Microsoft.UI.Xaml;
using System;
using System.Net;
using TrafficUI.Connection;
using System.Net.Sockets;
using System.Threading;
using System.Linq;
using System.Collections.Generic;
using System.Threading.Tasks;

// To learn more about WinUI, the WinUI project structure,
// and more about our project templates, see: http://aka.ms/winui-project-info.

namespace TrafficUI
{
    /// <summary>
    /// An empty window that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class MainWindow : Window
    {
        Thread mThread;
        PythonConnection pc;

        public MainWindow()
        {
            this.InitializeComponent();
        }

        int carcount = 0;
        int lkwcount = 0;


        private void myButton_Click(object sender, RoutedEventArgs e)
        {
            myButton.Content = "End Server";

            //AsyncServer.StartListening();
            pc = new PythonConnection();

            //Task.run
            ThreadStart ts = new ThreadStart(pc.GetInfo);
            mThread = new Thread(ts);
            mThread.Start();

            pc.OnRecievedMessage += MainWindow_OnRecievedMessage;
        }

        private void MainWindow_OnRecievedMessage(object sender, OnMessageHandler e)
        {

            var message = e.GetMessage();

            if (message == "lkw")
            {
                lkwcount++;
            }
            else if (message == "car")
            {
                carcount++;
            }

            this.DispatcherQueue.TryEnqueue(() =>
                statusPkwText.Text = "Cars: " + carcount.ToString()
            );

            this.DispatcherQueue.TryEnqueue(() =>
                statusLkwText.Text = "LKWs: " + lkwcount.ToString()
            );
        }

        private void pythonButton_Click(object sender, RoutedEventArgs e)
        {
            pc.SendMessage("end");
        }

        string actual = "lkw";
        private void carPwkButton_Click(object sender, RoutedEventArgs e)
        {
            if (actual == "lkw")
            {
                actual = "car";

            }
            else
            {
                actual = "lkw";
            }

            pc.SendMessage(actual);
        }
    }
}