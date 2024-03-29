/*

  EXAMPLE osmium_count

  Counts the number of nodes, ways, and relations in the input file.

  DEMONSTRATES USE OF:
  * OSM file input
  * your own handler
  * the memory usage utility class

  SIMPLER EXAMPLES you might want to understand first:
  * osmium_read

  LICENSE
  The code in this example file is released into the Public Domain.

*/

#include <cstdint> // for std::uint64_t
#include <cstdlib> // for std::exit
#include <filesystem>
#include <iostream> // for std::cout, std::cerr
#include <string>
#include <vector>
namespace fs = std::filesystem;

// Allow any format of input files (XML, PBF, ...)
#include <osmium/io/any_input.hpp>

// We want to use the handler interface
#include <osmium/handler.hpp>

// Utility class gives us access to memory usage information
#include <osmium/util/memory.hpp>

// For osmium::apply()
#include <osmium/visitor.hpp>

// For the location index. There are different types of indexes available.
// This will work for all input files keeping the index in memory.
#include <osmium/index/map/flex_mem.hpp>

// For the NodeLocationForWays handler
#include <osmium/handler/node_locations_for_ways.hpp>

// The type of index used. This must match the include file above
using index_type = osmium::index::map::FlexMem<osmium::unsigned_object_id_type,
                                               osmium::Location>;

// The location handler always depends on the index type
using location_handler_type = osmium::handler::NodeLocationsForWays<index_type>;

// Handler derive from the osmium::handler::Handler base class. Usually you
// overwrite functions node(), way(), and relation(). Other functions are
// available, too. Read the API documentation for details.
struct BlockageHandler : public osmium::handler::Handler {
    std::uint64_t nodes = 0;
    std::uint64_t ways = 0;
    std::uint64_t nodes_with_ways = 0;
    std::uint64_t relations = 0;

    // This callback is called by osmium::apply for each node in the data.
    void node(const osmium::Node& /*node*/) noexcept { ++nodes; }

    // This callback is called by osmium::apply for each way in the data.
    void way(const osmium::Way& way) noexcept {
        for (auto& node : way.nodes()) { nodes_with_ways++; }
        ++ways;
    }

    // This callback is called by osmium::apply for each relation in the data.
    void relation(const osmium::Relation& /*relation*/) noexcept {
        ++relations;
    }

}; // struct BlockageHandler

std::vector<std::string> paths() {
    std::vector<std::string> filepaths;
    std::string path = "imgs";
    for (const auto& entry : fs::directory_iterator(path))
        filepaths.push_back(entry.path());
    return filepaths;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " OSMFILE\n";
        std::exit(1);
    }

    try {
        // The Reader is initialized here with an osmium::io::File, but could
        // also be directly initialized with a file name.
        osmium::io::File input_file{argv[1]};
        osmium::io::Reader reader{input_file,
                                  osmium::osm_entity_bits::node |
                                      osmium::osm_entity_bits::way};

        // The index to hold node locations.
        index_type index;

        // The location handler will add the node locations to the index and then
        // to the ways
        location_handler_type location_handler{index};

        std::vector<std::string> files = paths();
        for (auto& path : files) { std::cout << path << std::endl; }

        // Create an instance of our own BlockageHandler and push the data from the
        // input file through it.
        BlockageHandler handler;
        osmium::apply(reader, location_handler, handler);

        // You do not have to close the Reader explicitly, but because the
        // destructor can't throw, you will not see any errors otherwise.
        reader.close();

        std::cout << "Nodes: " << handler.nodes << "\n";
        std::cout << "Ways: " << handler.ways << "\n";
        std::cout << "Nodes with ways: " << handler.nodes_with_ways << "\n";
        std::cout << "Relations: " << handler.relations << "\n";

        // Because of the huge amount of OSM data, some Osmium-based programs
        // (though not this one) can use huge amounts of data. So checking actual
        // memore usage is often useful and can be done easily with this class.
        // (Currently only works on Linux, not OSX and Windows.)
        osmium::MemoryUsage memory;

        std::cout << "\nMemory used: " << memory.peak() << " MBytes\n";
    } catch (const std::exception& e) {
        // All exceptions used by the Osmium library derive from std::exception.
        std::cerr << e.what() << '\n';
        std::exit(1);
    }
}
