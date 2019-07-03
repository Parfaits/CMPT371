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

void accept_handler(const boost::system::error_code &error)
{
  if (!error)
  {
    cout << "Connection made." << endl;
  }
  else
  {
  	cerr << "bruh what" << endl;
  }
}

int main()
{
	io_service ioservice;
	tcp::endpoint endpoint{tcp::v4(), PORT};
	tcp::acceptor accepting{ioservice, endpoint};
	tcp::socket sock{ioservice};
	sock.set_option(tcp::acceptor::reuse_address(true));
	try
	{
		sock.bind(endpoint, e);
	}
	catch(const exception &e)
	{
		cout << "wtf" << endl;
		cerr << e.what() << endl;
	}
	
	cout << "Ready boii" << endl;
	accepting.listen();
	accepting.async_accept(sock, accept_handler);
	cout << "Accepted " << sock.remote_endpoint().address().to_string() << endl;

	
	ioservice.run();
	return 0;
}