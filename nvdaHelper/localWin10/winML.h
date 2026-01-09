/*
Header for WinML (Windows Machine Learning) integration.
A part of NonVisual Desktop Access (NVDA)
Copyright (C) 2026 NV Access Limited
This file may be used under the terms of the GNU General Public License, version 2 or later.
For more details see: https://www.gnu.org/licenses/gpl-2.0.html

This module provides Windows Machine Learning support for ONNX Runtime,
enabling hardware-accelerated execution providers for AI models.
*/

#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#ifdef BUILDING_LOCALWIN10
#define WINML_API __declspec(dllexport)
#else
#define WINML_API __declspec(dllimport)
#endif

/**
 * Initialize the Windows Machine Learning environment and register execution providers.
 * This function creates an ONNX Runtime environment and registers all compatible
 * execution providers (DirectML, CUDA, etc.) available on the system.
 *
 * @return 0 if initialization succeeded, -1 otherwise.
 */
WINML_API int winML_initialize();

/**
 * Create an ONNX Runtime inference session.
 *
 * @param modelPath Path to the ONNX model file.
 * @param enableProfiling Whether to enable profiling (0 = disabled, non-zero = enabled).
 * @return Opaque session handle, or NULL on failure.
 */
WINML_API void* winML_createSession(const char* modelPath, int enableProfiling);

/**
 * Destroy an ONNX Runtime inference session.
 *
 * @param session The session handle to destroy.
 */
WINML_API void winML_destroySession(void* session);

/**
 * Get the number of input tensors for a session.
 *
 * @param session The session handle.
 * @return Number of inputs, or 0 on error.
 */
WINML_API int winML_getInputCount(void* session);

/**
 * Get the number of output tensors for a session.
 *
 * @param session The session handle.
 * @return Number of outputs, or 0 on error.
 */
WINML_API int winML_getOutputCount(void* session);

/**
 * Cleanup and release Windows Machine Learning resources.
 */
WINML_API void winML_terminate();

#ifdef __cplusplus
}
#endif
