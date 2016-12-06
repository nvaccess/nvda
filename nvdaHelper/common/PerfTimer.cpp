/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/
#include <stdexcept>
#include <sstream>
#include "PerfTimer.h"

std::map<std::string, PerfResult> PerfTimer::s_results = std::map<std::string, PerfResult>();

PerfTimer::PerfTimer(const std::string& name)
:m_pcFreq(0.0), m_counterStart(0), m_result(nullptr) {
	m_result = &(s_results[name]);
	StartCounter();
}

void PerfTimer::Stop() {
	if(m_result) {
		auto time = GetCounter();
		m_result->totalTime += time;
		m_result->numberOfHits += 1;
		m_result = nullptr;
	}
}

PerfTimer::~PerfTimer() {
	Stop();
}

std::map<std::string, PerfResult> PerfTimer::GetTimerDataAndReset() {
	auto result = s_results;
	s_results.clear();
	return result;
}

void PerfTimer::StartCounter() {
    LARGE_INTEGER li;
    if(!QueryPerformanceFrequency(&li)) {
    	throw std::runtime_error("QueryPerformanceFrequency failed");
    }

    m_pcFreq = double(li.QuadPart)/1000.0;

    QueryPerformanceCounter(&li);
    m_counterStart = li.QuadPart;
}
double PerfTimer::GetCounter() {
    LARGE_INTEGER li;
    QueryPerformanceCounter(&li);
    return double(li.QuadPart-m_counterStart)/m_pcFreq;
}

std::string PerfTimer::GetPerfResults() {
	auto perfResults = PerfTimer::GetTimerDataAndReset();
	std::stringstream sstream;
	sstream << "Perf Results\n";
	for(auto& result : perfResults){
		sstream << result.first << " Total time: " << result.second.totalTime 
		<< " Hit count: " << result.second.numberOfHits;
		if(result.second.totalTime > 0 && result.second.numberOfHits > 0) {
			sstream << " Average Time: " << result.second.totalTime / result.second.numberOfHits;
		}
		sstream << '\n';
	}
	return sstream.str();
}