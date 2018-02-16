
#include "spdlog/spdlog.h"

#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <iostream>
#include <string>
#include <memory>



namespace spd = spdlog;


namespace { // Avoid cluttering the global namespace.

  // A friendly class.
  class Logger
  {
    public:
      void info(const std::string& msg) const { this->_logger->info(msg); }
    protected:
      std::shared_ptr<spdlog::logger> _logger{};
  };


  class ConsoleLogger : public Logger
  {
  public:
      ConsoleLogger(const std::string& name) { this->_logger = spd::stdout_color_mt(name); }
  };

  class FileLogger : public Logger
  {
  public:
      FileLogger(const std::string& name, const std::string& file_path) { this->_logger = spd::basic_logger_mt(name, file_path); }
  };


  void close_all()
  {
      spdlog::drop_all();
  }

}

BOOST_PYTHON_MODULE(spdlog)
{
    using namespace boost::python;
    class_<ConsoleLogger>("ConsoleLogger", init<std::string>())
        // Add a regular member function.
        .def("info", &ConsoleLogger::info)
        ;
    class_<FileLogger>("FileLogger", init<std::string, std::string>())
        // Add a regular member function.
        .def("info", &ConsoleLogger::info)
        ;


    def("close_all", close_all);
}
