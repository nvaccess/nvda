use std::{env, path::Path};
use std::path::PathBuf;

fn main() {
    let manifest_dir = env::var("CARGO_MANIFEST_DIR").unwrap();
    println!(
        "cargo:rustc-link-search=native={}",
        Path::new(&manifest_dir).join("lib").display()
    );
    println!("cargo:rustc-link-lib=nvdaControllerClient");
    println!("cargo:rerun-if-changed=include/nvdaController.h");

    let bindings = bindgen::Builder::default()
        .header("include/nvdaController.h")
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
