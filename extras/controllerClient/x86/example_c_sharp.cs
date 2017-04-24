//example_c_sharp.cs
//A part of NonVisual Desktop Access (NVDA)
//Copyright (C) 2007-2017 NV Access Limited, DojoMike
//This file is covered by the GNU Lesser General Public License, version 2.1.
//See the file license.txt for more details.
using System;
using System.Runtime.InteropServices;
using System.Text;

namespace NVAccess
{
    /// <summary>
    /// C# wrapper class for the NVDA controller client DLL
    /// </summary>
    public static class NVDA
    {
        [DllImport("nvdaControllerClient32.dll")]
        private static extern int nvdaController_testIfRunning();

        [DllImport("nvdaControllerClient32.dll", CharSet = CharSet.Unicode)]
        private static extern int nvdaController_speakText(StringBuilder text);

        [DllImport("nvdaControllerClient32.dll")]
        private static extern int nvdaController_cancelSpeech();

        [DllImport("nvdaControllerClient32.dll")]
        private static extern int nvdaController_brailleMessage(StringBuilder text);
        
        /// <summary>
        /// Checks to see if NVDA is running
        /// </summary>
        public static bool IsRunning
        {
            get
            {
                return nvdaController_testIfRunning() == 0;
            }
        }

        /// <summary>
        /// Tells NVDA to speak a string of text
        /// </summary>
        /// <param name="text">The text to speak</param>
        /// <param name="interrupt">If true, NVDA will stop whatever it's saying at th emoment and immediately speak the string</param>
        public static void Say(string text, bool interrupt = false)
        {
            if (interrupt)
                Stop();

            StringBuilder sb = new StringBuilder(text.Length);
            sb.Append(text);
            nvdaController_speakText(sb);
        }

        /// <summary>
        /// Tells NVDA to braille a string of text (UNTESTED)
        /// </summary>
        /// <param name="text">The text to braille</param>
        /// <param name="interrupt">If true, NVDA will stop whatever it's brailling at the moment and immediately braille the string</param>
        public static void Braille(string text, bool interrupt)
        {
            if (interrupt)
                Stop();

            StringBuilder sb = new StringBuilder(text.Length);
            sb.Append(text);
            nvdaController_brailleMessage(sb);
        }
        
        /// <summary>
        /// Tells NVDA to stop talking
        /// </summary>
        public static void Stop()
        {
            nvdaController_cancelSpeech();
        }
    }
}
