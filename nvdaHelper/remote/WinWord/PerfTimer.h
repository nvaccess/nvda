#include <windows.h>
#include <map>

class PerfResult{
public:
	PerfResult()
	: totalTime(0), numberOfHits(0)
	{ }
	double totalTime;
	unsigned int numberOfHits;
};

class PerfTimer {
public:
	PerfTimer(const std::string& name);

	void Stop();

	~PerfTimer();

	static std::map<std::string, PerfResult> GetTimerDataAndReset();

	static std::string GetPerfResults();

private:
	void StartCounter();
	double GetCounter();

	double m_pcFreq;
	unsigned __int64 m_counterStart;
	PerfResult* m_result;
	static std::map<std::string, PerfResult> s_results;
};