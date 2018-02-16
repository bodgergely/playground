
#include "spdlog/spdlog.h"
#include <memory>
#include <string>
#include <cstdlib>
#include <time.h>

namespace spd = spdlog;
using namespace std;

void async_example()
{
    size_t q_size = 4096; //queue size must be power of 2
    spdlog::set_async_mode(q_size);
    auto async_file = spd::daily_logger_st("async_file_logger", "logs/my_async_log.txt");
    for (int i = 0; i < 100; ++i)
        async_file->info("Async message #{}", i);
}


class StringLogger
{
public:
    StringLogger(const string& file_path, const string& logger_name, bool async=true)
    {
        if(async)
        {
            size_t q_size = 4096; //queue size must be power of 2
            spdlog::set_async_mode(q_size);
            _logger = spd::daily_logger_st(logger_name, file_path);
        }
        else
        {
            _logger = spd::daily_logger_mt(logger_name, file_path);
        }
    }
    ~StringLogger()
    {
    }

    char generate_char()
    {
        return 'a' + (char)(rand() % 27);
    }
    
    string generate_message(int len)
    {
       srand(time(NULL)); 
       string msg{""};
       for(int i=0;i<len;i++)
       {
          char c = generate_char();
          msg.push_back(c);
       }
       return msg;
    } 

    void run(int num_logs, int msg_len)
    {
       string msg = generate_message(msg_len);
       for(int i =0;i<num_logs;i++)
       {
           _logger->info(msg);
       } 
    }

private:
    std::shared_ptr<spdlog::logger> _logger;
};


int main(int argc, char** argv)
{
    StringLogger slogger("logs/stringlogger.log", "stringlogger", false);
    int log_count = 100000;
    int msg_len = 1000;
    slogger.run(log_count, msg_len);
    return 0;
}
