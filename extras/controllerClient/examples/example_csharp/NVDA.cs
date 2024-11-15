// Copyright(C) 2017-2023 NV Access Limited, Arnold Loubriat, Leonard de Ruijter
// This file is covered by the GNU Lesser General Public License, version 2.1.
// See the file license.txt for more details.

using System;
using System.ComponentModel;
using System.Runtime.InteropServices;

namespace NVAccess.NVDA
{
    /// <summary>
    /// C# wrapper class for the NVDA controller client DLL.
    /// </summary>
    static class NVDA
    {
        [DllImport("nvdaControllerClient.dll", CharSet = CharSet.Unicode)]
        private static extern int nvdaController_brailleMessage(string message);

        [DllImport("nvdaControllerClient.dll")]
        private static extern int nvdaController_cancelSpeech();

        [DllImport("nvdaControllerClient.dll", CharSet = CharSet.Unicode)]
        private static extern int nvdaController_speakText(string text);

        [DllImport("nvdaControllerClient.dll")]
        private static extern int nvdaController_testIfRunning();

        [DllImport("nvdaControllerClient.dll", CharSet = CharSet.Unicode)]
        private static extern int nvdaController_getProcessId(out uint processId);

        [DllImport("nvdaControllerClient.dll", CharSet = CharSet.Unicode)]
        private static extern int nvdaController_speakSsml(
            string ssml,
            SymbolLevel symbolLevel = SymbolLevel.Unchanged,
            SpeechPriority priority = SpeechPriority.Normal,
            bool asynchronous = true
        );

        [UnmanagedFunctionPointer(CallingConvention.Winapi, CharSet = CharSet.Unicode)]
        public delegate int OnSsmlMarkReached(string mark);

        [DllImport("nvdaControllerClient.dll", CharSet = CharSet.Unicode)]
        private static extern int nvdaController_setOnSsmlMarkReachedCallback(OnSsmlMarkReached callback);

        /// <summary>
        /// Indicates whether NVDA is running.
        /// </summary>
        public static bool IsRunning => nvdaController_testIfRunning() == 0;

        /// <summary>
        /// Tells NVDA to braille a message.
        /// </summary>
        /// <param name="message">The message to braille.</param>
        public static void Braille(string message)
        {
            int res = nvdaController_brailleMessage(message);
            if (res != 0)
            {
                throw new Win32Exception(res);
            }

        }

        /// <summary>
        /// Tells NVDA to immediately stop speaking.
        /// </summary>
        public static void CancelSpeech()
        {
            int res = nvdaController_cancelSpeech();
            if (res != 0)
            {
                throw new Win32Exception(res);
            }

        }

        /// <summary>
        /// Tells NVDA to speak some text.
        /// </summary>
        /// <param name="text">The text to speak.</param>
        /// <param name="interrupt">If true, NVDA will immediately speak the text, interrupting whatever it was speaking before.</param>
        public static void Speak(string text, bool interrupt = true)
        {
            if (interrupt)
            {
                CancelSpeech();
            }
            int res = nvdaController_speakText(text);
            if (res != 0)
            {
                throw new Win32Exception(res);
            }
        }

        /// <summary>
        /// Instructs NVDA to speak the given Speech Synthesis Markup Language (SSML).
        /// </summary>
        /// <param name="ssml">The ssml to speak.</param>
        /// <param name="symbolLevel">The symbol verbosity level.</param>
        /// <param name="priority">The priority of the speech sequence.</param>
        /// <param name="asynchronous">Whether SSML should be spoken asynchronously.</param>
        public static void SpeakSsml(
            string ssml,
            SymbolLevel symbolLevel = SymbolLevel.Unchanged,
            SpeechPriority priority = SpeechPriority.Normal,
            bool asynchronous = true,
            OnSsmlMarkReached callback = null
        )
        {
            int res = NVDA.nvdaController_setOnSsmlMarkReachedCallback(callback);
            if (res != 0)
            {
                throw new Win32Exception(res);
            }
            res = nvdaController_speakSsml(ssml, symbolLevel, priority, asynchronous);
            if (res != 0)
            {
                throw new Win32Exception(res);
            }
            res = NVDA.nvdaController_setOnSsmlMarkReachedCallback(null);
            if (res != 0)
            {
                throw new Win32Exception(res);
            }
        }

        /// <summary>
        /// Retrieves the process identifier (PID) of NVDA's process.
        /// </summary>
        /// <returns></returns>
        public static uint GetProcessId()
        {
            uint pid;
            int res = nvdaController_getProcessId(out pid);
            if (res != 0)
            {
                throw new Win32Exception(res);
            }
            return pid;
        }
    }
}
