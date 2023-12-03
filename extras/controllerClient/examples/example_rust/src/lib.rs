// A part of NonVisual Desktop Access (NVDA)
// Copyright (C) 2023 NV Access Limited, Leonard de Ruijter
// This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
// For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

mod bindgen;

pub use bindgen::{error_status_t, wchar_t};
use bindgen::{
    nvdaController_brailleMessage, nvdaController_cancelSpeech, nvdaController_getProcessId,
    nvdaController_setOnSsmlMarkReachedCallback, nvdaController_speakSsml,
    nvdaController_speakText, nvdaController_testIfRunning, onSsmlMarkReachedFuncType,
    SPEECH_PRIORITY, SYMBOL_LEVEL,
};
use windows::{
    core::{Result, HSTRING},
    Win32::Foundation::WIN32_ERROR,
};

#[repr(u32)]
#[derive(Debug, Copy, Clone, Hash, PartialEq, Eq)]
pub enum SpeechPriority {
    Normal = 0,
    Next = 1,
    Now = 2,
}

#[repr(i32)]
#[derive(Debug, Copy, Clone, Hash, PartialEq, Eq)]
pub enum SymbolLevel {
    None = 0,
    Some = 100,
    Most = 200,
    All = 300,
    Char = 1000,
    Unchanged = -1,
}

pub type OnSsmlMarkReached = onSsmlMarkReachedFuncType;

fn to_result(error: u32) -> Result<()> {
    WIN32_ERROR(error).ok()
}

pub fn test_if_running() -> Result<()> {
    let res = unsafe { nvdaController_testIfRunning() };
    to_result(res)
}

pub fn cancel_speech() -> Result<()> {
    let res = unsafe { nvdaController_cancelSpeech() };
    to_result(res)
}

pub fn speak_text(text: &str, interrupt: bool) -> Result<()> {
    if interrupt {
        cancel_speech()?;
    }
    let text = HSTRING::from(text);
    let res = unsafe { nvdaController_speakText(text.as_ptr()) };
    to_result(res)
}

pub fn braille_message(message: &str) -> Result<()> {
    let message = HSTRING::from(message);
    let res = unsafe { nvdaController_brailleMessage(message.as_ptr()) };
    to_result(res)
}

pub fn get_process_id() -> Result<u32> {
    let mut pid: u32 = 0;
    let res = unsafe { nvdaController_getProcessId(&mut pid) };
    to_result(res)?;
    Ok(pid)
}

fn set_on_ssml_mark_reached_callback(callback: OnSsmlMarkReached) -> Result<()> {
    let res = unsafe { nvdaController_setOnSsmlMarkReachedCallback(callback) };
    to_result(res)
}

pub fn speak_ssml(
    ssml: &str,
    symbol_level: SymbolLevel,
    priority: SpeechPriority,
    asynchronous: bool,
    callback: onSsmlMarkReachedFuncType,
) -> Result<()> {
    if callback.is_some() {
        set_on_ssml_mark_reached_callback(callback)?;
    }
    let ssml = HSTRING::from(ssml);
    let res = unsafe {
        nvdaController_speakSsml(
            ssml.as_ptr(),
            symbol_level as SYMBOL_LEVEL,
            priority as SPEECH_PRIORITY,
            asynchronous.into(),
        )
    };
    if callback.is_some() {
        set_on_ssml_mark_reached_callback(None)?;
    }
    to_result(res)
}
