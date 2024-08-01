/*
This file is a part of the NVDA project.
URL: http://github.com/nvaccess/nvda/
Copyright 2023 NV Access Limited.
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License version 2.0, as published by
	the Free Software Foundation.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <concepts>
#include <vector>
#include <algorithm>
#include <ranges>
#include <variant>
#include <uiautomation.h>
#include <comutil.h>

/// @brief creates a vector of ints from a SAFEARRAY.
/// @param pSafeArray
/// @return the vector of ints.
std::vector<int> SafeArrayToVector(SAFEARRAY* pSafeArray);

/// @brief Fetches the runtimeID from a given uI Automation element.
/// @param pElement the UI Automation element whose runtime ID should be fetched.
/// @return the runtime ID from the element.
std::vector<int> getRuntimeIDFromElement(IUIAutomationElement* pElement);

// @brief a helper template function for the supports_alternative concept.
template <typename T, typename V, std::size_t... indexes>
constexpr bool supports_alternative_impl(std::index_sequence<indexes...>) {
    return (std::same_as<T, std::variant_alternative_t<indexes, V>> || ...);
}

// @brief a concept that checks if a given type can be held by a given variant type.
// @tparam T the type to check
// @tparam V the variant type to check
template<typename T, typename V>
concept supports_alternative = supports_alternative_impl<T, V>(std::make_index_sequence<std::variant_size_v<V>>{});
