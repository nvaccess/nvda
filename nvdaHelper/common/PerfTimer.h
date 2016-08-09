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
#ifndef NVDAHELPER_COMMON_PERFTIMER_H
#define NVDAHELPER_COMMON_PERFTIMER_H

#include <windows.h>
#include <map>

/*
* Holds the results of monitoring performance for a section of code.
*/
class PerfResult{
public:
	PerfResult()
	: totalTime(0), numberOfHits(0)
	{ }
	double totalTime; ///< The total time spend in the monitored section of code
	unsigned int numberOfHits; ///< The total number of times that the section is hit.
};

/*
* Allows performance of a section of code to be monitored.
* Supports RAII based timing, ie will start on construction and stop on destruction.
*/
class PerfTimer {
public:
	/* Ctor. Starts the timer, will store the result against the name given in the parameter
	* @param name the name for the section of code to be timed. Use different names for different sections.
	*/
	PerfTimer(const std::string& name);

	/* Dtor. Stops the timer if it is not already stopped.
	*/
	~PerfTimer();

	/* Manually stop the timer. Useful if the section of code to be timed is not tied to the scope of the PerfTimer object.
	*/
	void Stop();

	/* Get the timer results, and resets the currently stored results.
	* Ensure that all created timers have been stopped (or destructed) before calling.
	*/
	static std::map<std::string, PerfResult> GetTimerDataAndReset();

	/* Get the performance results pre formated, clears the results
	* Ensure that all created timers have been stopped (or destructed) before calling.
	*/
	static std::string GetPerfResults();

private:
	void StartCounter();
	double GetCounter();

	double m_pcFreq; ///< CPU frequency as reported by Windows.
	unsigned __int64 m_counterStart; ///< Windows performance timer value when the timer was started.
	PerfResult* m_result; ///< The result for this instance of the timer.
	static std::map<std::string, PerfResult> s_results; ///< The results being collected.
};

#endif