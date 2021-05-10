using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace TrafficUI.Connection
{



    public class PythonConnection
    {
        public string connectionIP = "127.0.0.1";
        public int connectionPort = 25001;
        IPAddress localAdd;
        TcpListener listener;
        TcpClient client;
        //Vector3 receivedPos = Vector3.zero;

        bool running;

        public void GetInfo()
        {
            localAdd = IPAddress.Parse(connectionIP);
            listener = new TcpListener(IPAddress.Any, connectionPort);
            listener.Start();

            client = listener.AcceptTcpClient();

            running = true;
            while (running)
            {
                SendAndReceiveData();
            }

            listener.Stop();
        }

        public void StopServer()
        {
            running = false;
        }


        void SendAndReceiveData()
        {
            NetworkStream nwStream = client.GetStream();
            byte[] buffer = new byte[client.ReceiveBufferSize];

            //---receiving Data from the Host----
            int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
            string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string

            if (dataReceived != null)
            {
                //---Using received data---
                //receivedPos = StringToVector3(dataReceived); //<-- assigning receivedPos value from Python                                                             //print("received pos data, and moved the Cube!");
                OnRecievedMessage(this, new OnMessageHandler(dataReceived));           
            }
        }

        public void SendMessage(string message)
        {
            NetworkStream nwStream = client.GetStream();

            //---Sending Data to Host----
            byte[] myWriteBuffer = Encoding.ASCII.GetBytes(message); //Converting string to byte data
            nwStream.Write(myWriteBuffer, 0, myWriteBuffer.Length); //Sending the data in Bytes to Python
        }


        /// <summary>Called after a message was sent</summary>
        public event EventHandler<OnMessageHandler> OnRecievedMessage;

    /*
    public static Vector3 StringToVector3(string sVector)
    {
        // Remove the parentheses
        if (sVector.StartsWith("(") && sVector.EndsWith(")"))
        {
            sVector = sVector.Substring(1, sVector.Length - 2);
        }

        // split the items
        string[] sArray = sVector.Split(',');

        // store as a Vector3
        Vector3 result = new Vector3(
            float.Parse(sArray[0]),
            float.Parse(sArray[1]),
            float.Parse(sArray[2]));

        return result;
    }*/
    /*
    public static string GetLocalIPAddress()
    {
        var host = Dns.GetHostEntry(Dns.GetHostName());
        foreach (var ip in host.AddressList)
        {
            if (ip.AddressFamily == AddressFamily.InterNetwork)
            {
                return ip.ToString();
            }
        }
        throw new System.Exception("No network adapters with an IPv4 address in the system!");
    }
    */
}


    /// <summary>
    /// Handler for when a message was send to a client
    /// </summary>
    public class OnMessageHandler : EventArgs
    {

        /// <summary>The message that was sent to the client</summary>
        private string _message;

        /// <summary>Create a new handler for when a message was sent</summary>
        /// <param name="Client">The client the message was sent to</param>
        /// <param name="Message">The message that was sent to the client</param>
        public OnMessageHandler(string Message)
        {
            _message = Message;
        }

        /// <summary>The message that was send to the client</summary>
        /// <returns>The sent message</returns>
        public string GetMessage()
        {
            return _message;
        }
    }
}