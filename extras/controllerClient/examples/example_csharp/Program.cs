// Copyright(C) 2017-2023 NV Access Limited, Arnold Loubriat, Leonard de Ruijter
// This file is covered by the GNU Lesser General Public License, version 2.1.
// See the file license.txt for more details.

using System;
using System.Text;
using System.Threading.Tasks;

namespace NVAccess.NVDA
{
    class Program
    {
        static async Task Main(string[] args)
        {
            // Test if NVDA is running.
            if (!NVDA.IsRunning)
            {
                Console.Error.WriteLine("Error communicating with NVDA.");
            }
            else
            {
                Console.WriteLine($"NVDA is running as process {NVDA.GetProcessId()}");
                // Speak and braille some messages.
                for (int i = 0; i < 4; i++)
                {
                    NVDA.Speak("This is a test client for NVDA!");
                    NVDA.Braille($"Time: {0.75 * i} seconds.");
                    await Task.Delay(625);
                    NVDA.CancelSpeech();
                }

                int onMarkReached(string name)
                {
                    Console.WriteLine($"Reached SSML mark with name: {name}");
                    return 0;
                }


                StringBuilder ssmlBuilder = new StringBuilder();
                ssmlBuilder
                    .Append("<speak>")
                    .Append("This is one sentence.")
                    .Append("<mark name=\"test\" />")
                    .Append("<prosody pitch=\"200%\">This sentence is pronounced with higher pitch.</prosody>")
                    .Append("<mark name=\"test2\" />")
                    .Append("This is a third sentence.")
                    .Append("<mark name=\"test3\" />")
                    .Append("This is a fourth sentence. We will stay silent for a second after this one.")
                    .Append("<break time=\"1000ms\" />")
                    .Append("<mark name=\"test4\" />")
                    .Append("This is a fifth sentence.")
                    .Append("<mark name=\"test5\" />")
                    .Append("</speak>");

                NVDA.SpeakSsml(ssmlBuilder.ToString(), asynchronous: false, callback: onMarkReached);
                NVDA.Braille("Test completed!");
            }
            Console.ReadKey(true);
        }
    }
}
