#include <string>
#include <memory>

#include "genfile/bgen/bgen.hpp"

struct VariantInfo {
    std::string snpid;
    std::string rsid;
    std::string chromosome;
    uint32_t position;
    std::vector<std::string> alleles;
};

class BgenParser {
public:
    
    BgenParser();
    
    void init(std::string bgenFilePath);
    
    void readVariantProbs(uint64_t variantFileStartPosition, float* probsArray);
        
    size_t nSamples;
    
    size_t nVariants;
    
private:
    
    std::unique_ptr<std::istream> m_stream;
    
    genfile::bgen::Context m_context;
    
    VariantInfo m_variantInfo;
    
    std::vector<genfile::byte_t> m_buffer1;
    
    std::vector<genfile::byte_t> m_buffer2;
    
    static const size_t N_PROBS_PER_SAMPLE = 3;
};