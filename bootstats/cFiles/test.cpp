#include "Bootstrap.hpp"
#include <ctime>

int main() {

  // Initialize constants
  const size_t NSamples(400), NBinSize(5), NConfigs(1000), NVars(128*4);
  const size_t NSize(NConfigs/NBinSize);
  const size_t NTimes(50);

  // Initialize data
  const mat<double> dData(NConfigs, vec<double>(NVars, 1));

  // Create Bootstrapper instance
  Bootstrapper<double> dBs(dData, NSamples, NSize, NBinSize);

  // Create vector for time measurements
  vec<double> timings(NTimes, 0);
  // Measure kernel operation
  for(size_t nt=0; nt<NTimes; nt++){
    const std::clock_t start = std::clock();
    dBs.getSamples();
    const std::clock_t end = std::clock();
    timings[nt] = double(end-start)/CLOCKS_PER_SEC;
  }

  // Compute timings mean
  const double mean(
    std::accumulate(
      timings.begin(), 
      timings.end(), 
      double(0)
    )/static_cast<double>(timings.size())
  );

  // Compute timings sdev
  const double sdev(
    std::sqrt(std::accumulate(
      timings.begin(), 
      timings.end(), 
      double(0),
      [&](const double init, const double t){
        const double diff(t-mean);
        return init + diff*diff;
      }
    )/static_cast<double>(timings.size()-1))
  );

  std::cout<<"t = "<<mean<<" +/- "<<sdev<<" [s]"<<std::endl;

  return 1;
}
