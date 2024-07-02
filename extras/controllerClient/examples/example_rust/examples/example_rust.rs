// A part of NonVisual Desktop Access (NVDA)
// Copyright (C) 2023 NV Access Limited, Leonard de Ruijter
// This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
// For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

use nvda::{error_status_t, wchar_t, SpeechPriority, SymbolLevel};
use std::thread::sleep;
use std::time::Duration;
use windows::core::{Result, PWSTR};

#[no_mangle]
unsafe extern "C" fn on_mark_reached(name: *const wchar_t) -> error_status_t {
    let name = PWSTR::from_raw(name as _);
    println!("Reached SSML mark with name: {}", name.to_string().unwrap());
    0
}

fn main() -> Result<()> {
    // Test if NVDA is running.
    nvda::test_if_running().expect("Error communicating with NVDA.");
    println!("NVDA is running as process {}", nvda::get_process_id()?);

    // Speak and braille some messages.
    for i in 0..4 {
        nvda::speak_text("This is a test client for NVDA!", false)?;
        nvda::braille_message(format!("Time: {} seconds.", 0.75 * (i as f32)).as_str())?;
        sleep(Duration::from_millis(625));
        nvda::cancel_speech()?;
    }

    let ssml = r#"
        <speak>
            This is one sentence.
            <mark name="test" />
            <prosody pitch="200%">This sentence is pronounced with higher pitch.</prosody>
            <mark name="test2" />
            This is a third sentence.
            <mark name="test3" />
            This is a fourth sentence. We will stay silent for a second after this one.
            <break time="1000ms" />
            <mark name="test4" />
            This is a fifth sentence.
            <mark name="test5" />
        </speak>
    "#;
    nvda::speak_ssml(
        ssml,
        SymbolLevel::Unchanged,
        SpeechPriority::Normal,
        false,
        Some(on_mark_reached),
    )?;
    nvda::braille_message("Test completed!")?;
    Ok(())
}
