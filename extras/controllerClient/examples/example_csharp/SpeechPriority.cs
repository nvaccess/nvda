// Copyright(C) 2017-2023 NV Access Limited, Arnold Loubriat, Leonard de Ruijter
// This file is covered by the GNU Lesser General Public License, version 2.1.
// See the file license.txt for more details.

namespace NVAccess.NVDA
{
    /// <summary>
    /// Facilitates the ability to prioritize speech.
    /// This should match the SPEECH_PRIORITY enum in nvdaController.h, which itself matches the speech.priorities.SpeechPriority enum in NVDA.
    /// </summary>
    public enum SpeechPriority
    {
        /// <summary>
        /// Indicates that a speech sequence should have normal priority.
        /// </summary>
        Normal = 0,
        /// <summary>
        /// Indicates that a speech sequence should be spoken after the next utterance of lower priority is complete.
        /// </summary>
        Next = 1,
        /// <summary>
        /// Indicates that a speech sequence is very important and should be spoken right now,
        /// interrupting low priority speech.
        /// After it is spoken, interrupted speech will resume.
        /// Note that this does not interrupt previously queued speech at the same priority.
        /// </summary>
        Now = 2
    }
}
