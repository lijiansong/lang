#include <iostream>

#if 0
  class ASTDumper {
    /// Dump a child of the current node.
    template<typename Fn> void dumpChild(Fn doDumpChild) {
      // If we're at the top level, there's nothing interesting to do; just
      // run the dumper.
      if (TopLevel) {
        TopLevel = false;
        doDumpChild();
        while (!Pending.empty()) {
          Pending.back()(true);
          Pending.pop_back();
        }
        Prefix.clear();
        OS << "\n";
        TopLevel = true;
        return;
      }

      const FullComment *OrigFC = FC;
      auto dumpWithIndent = [this, doDumpChild, OrigFC](bool isLastChild) {
        // Print out the appropriate tree structure and work out the prefix for
        // children of this node. For instance:
        //
        //   A        Prefix = ""
        //   |-B      Prefix = "| "
        //   | `-C    Prefix = "|   "
        //   `-D      Prefix = "  "
        //     |-E    Prefix = "  | "
        //     `-F    Prefix = "    "
        //   G        Prefix = ""
        //
        // Note that the first level gets no prefix.
        {
          OS << '\n';
          ColorScope Color(*this, IndentColor);
          OS << Prefix << (isLastChild ? '`' : '|') << '-';
          this->Prefix.push_back(isLastChild ? ' ' : '|');
          this->Prefix.push_back(' ');
        }

        FirstChild = true;
        unsigned Depth = Pending.size();

        FC = OrigFC;
        doDumpChild();

        // If any children are left, they're the last at their nesting level.
        // Dump those ones out now.
        while (Depth < Pending.size()) {
          Pending.back()(true);
          this->Pending.pop_back();
        }

        // Restore the old prefix.
        this->Prefix.resize(Prefix.size() - 2);
      };

      if (FirstChild) {
        Pending.push_back(std::move(dumpWithIndent));
      } else {
        Pending.back()(false);
        Pending.back() = std::move(dumpWithIndent);
      }
      FirstChild = false;
    }
};
#endif

#define FORMAT_INDENT(indent)                                                  \
  {                                                                            \
    std::cout.width((indent));                                                 \
    std::cout << std::left << "";                                              \
    std::cout.unsetf(std::ios::adjustfield);                                   \
  }

int main() {
  int indent = 0;
  FORMAT_INDENT(indent);
  std::cout << "Program\n";
  indent += strlen("Program");
  FORMAT_INDENT(indent);
  std::cout << "DeclList\n";
  indent += strlen("DeclList");
  FORMAT_INDENT(indent);
  std::cout << "StmtList\n";
  return 0;
}
