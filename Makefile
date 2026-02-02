# CEPAC Makefile
# Supports incremental builds for faster development

CXX = g++
CXXFLAGS = -std=c++11 -O3 -Wall
TARGET = cepac

# Find all source and header files
SRCS = $(wildcard *.cpp)
HDRS = $(wildcard *.h)
OBJS = $(SRCS:.cpp=.o)

# Default target
all: $(TARGET)

# Link object files to create executable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Compile source files to object files
%.o: %.cpp $(HDRS)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Clean build artifacts
clean:
	rm -f $(OBJS) $(TARGET)

# Rebuild from scratch
rebuild: clean all

# Run the model (uses current directory for inputs)
run: $(TARGET)
	./$(TARGET)

# Show file counts
info:
	@echo "Source files: $(words $(SRCS))"
	@echo "Header files: $(words $(HDRS))"
	@echo "Object files: $(words $(OBJS))"

.PHONY: all clean rebuild run info
