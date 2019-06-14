#include <boost/asio/io_service.hpp>
#include <boost/asio/write.hpp>
#include <boost/asio/buffer.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <boost/exception/all.hpp>
#include <boost/asio.hpp>
#include <chrono>
#include <exception>
#include <thread>
#include <array>
#include <iostream>

#ifndef PORT
#define PORT 42069
#endif

using namespace boost::asio;
using std::cout;
using std::endl;
using std::to_string;
using std::string;
using std::cerr;
using std::exception;
using ip::tcp;

const string server_ipv4 = "142.58.15.118";

boost::system::error_code e;

// Messaging protocol
string read_all(tcp::socket &Sock) {
       streambuf buf;
       read_until( Sock, buf, "\n" );
       string data = buffer_cast<const char*>(buf.data());
       return data;
}
void send_all(tcp::socket &Sock, const string &message) {
       const string msg = message + "\n";
       write( Sock, buffer(message) );
}
// End messaging protocol

int main()
{
	io_service ioservice;
	tcp::socket sock{ioservice};
	tcp::endpoint endpoint{ip::address::from_string(server_ipv4), PORT};
	sock.connect(endpoint);

	
	return 0;
}