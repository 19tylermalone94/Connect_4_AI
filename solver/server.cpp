#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <boost/asio/io_context.hpp>
#include <iostream>
#include <string>
#include "Solver.hpp"

using namespace GameSolver::Connect4;
namespace beast = boost::beast;
namespace http = beast::http;
namespace net = boost::asio;
using tcp = net::ip::tcp;

// Function to create a simple HTTP server and integrate Connect4 solver
void run_http_server(unsigned short port) {
  net::io_context ioc;
  tcp::acceptor acceptor{ioc, {tcp::v4(), port}};
  tcp::socket socket{ioc};

  Solver solver;
  std::string opening_book = "7x6.book";
  solver.loadBook(opening_book);

  while (true) {
    acceptor.accept(socket);

    beast::flat_buffer buffer;
    http::request<http::string_body> req;
    http::read(socket, buffer, req);

    Position P;
    std::string line = req.body();
    std::string response_body;

    if (P.play(line) != line.size()) {
      response_body = "Error: Invalid move sequence.";
    } else {
      std::vector<int> score = solver.analyze(P, false);
      std::string score_str = "";
      for (int i = 0; i < Position::WIDTH; i++) {
        score_str += std::to_string(score[i]) + " ";
      }
      response_body = score_str;
    }

    http::response<http::string_body> res{http::status::ok, req.version()};
    res.set(http::field::server, "C++ Connect4 Server");
    res.set(http::field::content_type, "text/plain");
    res.body() = response_body;
    res.prepare_payload();

    http::write(socket, res);

    socket.shutdown(tcp::socket::shutdown_send);
    socket.close();
  }
}

int main() {
  try {
    run_http_server(8080);
  } catch (std::exception& e) {
    std::cerr << "Exception: " << e.what() << "\n";
  }
  return 0;
}
