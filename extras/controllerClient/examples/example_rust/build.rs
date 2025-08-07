// A part of NonVisual Desktop Access (NVDA)
// Copyright (C) 2023 NV Access Limited, Leonard de Ruijter
// This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
// For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

use std::path::PathBuf;
use std::{env, path::Path};

fn main() {
    let manifest_dir: &str = &env::var("CARGO_MANIFEST_DIR").unwrap();
    let architecture = env::var("CARGO_CFG_TARGET_ARCH").unwrap();
    let architecture: &str = match architecture.as_str() {
        "aarch64" => "arm64",
        "x86_64" => "x64",
        a => a,
    };
    let architecture_dir = Path::new(manifest_dir)
        .join("..")
        .join("..")
        .join(architecture)
        .canonicalize()
        .expect("Couldn't find architecture directory!");
    println!(
        "cargo:rustc-link-search=native={}",
        architecture_dir.display()
    );
    println!("cargo:rustc-link-lib=nvdaControllerClient");
    let header_file = architecture_dir.join("nvdaController.h");
    println!("cargo:rerun-if-changed={}", header_file.display());

    let bindings = bindgen::Builder::default()
        .header(header_file.display().to_string())
        .parse_callbacks(Box::new(bindgen::CargoCallbacks::new()))
        .allowlist_function("nvdaController_.+")
        .prepend_enum_name(false)
        .must_use_type("error_status_t")
        .generate()
        .expect("Unable to generate bindings");

    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings!");
}
