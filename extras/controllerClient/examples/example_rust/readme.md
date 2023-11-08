# NVDA Rust Example

This Rust workspace contains example code to interface with `nvdaControllerClient`.
To get started:

1. In the `bindgen` crate folder:
	* Add a `lib` folder containing `nvdaControllerClient.lib` matching the architecture of your Rust toolchain
	* Add a `include` folder containing `nvdaController.h`
1. Run `cargo test`. While this workspace has no tests, it ensures that our example is build
1. Copy ``nvdaControllerClient.dll` to `target/debug/examples`
1. Run `cargo run --example example_rust`
