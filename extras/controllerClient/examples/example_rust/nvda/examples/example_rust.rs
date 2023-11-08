use nvda::{error_status_t, wchar_t, SpeechPriority, SymbolLevel};
use std::thread::sleep;
use std::time::Duration;
use windows::core::PWSTR;

#[no_mangle]
unsafe extern "C" fn on_mark_reached(name: *const wchar_t) -> error_status_t {
    let name = PWSTR::from_raw(name as _);
    println!("Reached SSML mark with name: {}", name.to_string().unwrap());
    0
}

fn main() {
    // Test if NVDA is running.
    nvda::test_if_running().expect("Error communicating with NVDA.");
    println!(
        "NVDA is running as process {}",
        nvda::get_process_id().unwrap()
    );

    // Speak and braille some messages.
    for i in 0..4 {
        nvda::speak_text("This is a test client for NVDA!", false).unwrap();
        nvda::braille_message(format!("Time: {} seconds.", 0.75 * (i as f32)).as_str()).unwrap();
        sleep(Duration::from_millis(625));
        nvda::cancel_speech().unwrap();
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
    )
    .unwrap();
    nvda::braille_message("Test completed!").unwrap();
}
