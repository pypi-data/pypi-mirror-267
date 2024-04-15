#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <mqueue.h>
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

namespace nb = nanobind;

struct MQueue {
    mqd_t mqd;
    const int o_rdonly = O_RDONLY;
    const int o_wronly = O_WRONLY;
    const int o_rdwr = O_RDWR;
    const int o_creat = O_CREAT;
    const int o_excl = O_EXCL;
    const int o_nonblock = O_NONBLOCK;

    MQueue() : mqd((mqd_t)-1) {}

    int py_mq_open(const char *name, int oflag, unsigned int mode, struct mq_attr *attr) {
        mqd = mq_open(name, oflag, (mode_t)mode, attr);
        if (mqd == (mqd_t)-1) {
            return -1;
        } else {
            return 0;
        }
    }
    int py_mq_unlink(const char *name) {
        return mq_unlink(name);
    }
    int py_mq_close() {
        return mq_close(mqd);
    }
    int py_mq_send(std::string &msg, unsigned int msg_prio) {
        return mq_send(mqd, (const char *)msg.c_str(), msg.size(), msg_prio);
    }
    std::string py_mq_receive() {
        unsigned int msg_prio;
        std::string msg(32, '\0');
        mq_receive(mqd, (char *)msg.c_str(), msg.size(), &msg_prio);
        return msg;
    }
};
