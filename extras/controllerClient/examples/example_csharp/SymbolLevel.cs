// Copyright(C) 2017-2023 NV Access Limited, Arnold Loubriat, Leonard de Ruijter
// This file is covered by the GNU Lesser General Public License, version 2.1.
// See the file license.txt for more details.

namespace NVAccess.NVDA
{
    /// <summary>
    /// The desired symbol level in a speech sequence.
    /// This should match the SYMBOL_LEVEL enum in nvdaController.h, which itself matches the characterProcessing.SymbolLevel enum in NVDA.
    /// </summary>
    public enum SymbolLevel
    {
        None = 0,
        Some = 100,
        Most = 200,
        All = 300,
        Char = 1000,
        Unchanged = -1
    }
}
