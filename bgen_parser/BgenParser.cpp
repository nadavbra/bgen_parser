#include <sstream>
#include <fstream>

#include "BgenParser.h"

using std::vector;
using std::string;
using std::stringstream;
using std::ifstream;
using std::invalid_argument;
using std::runtime_error;

class ProbArraySetter {
public:

    ProbArraySetter(float* probArray, size_t probArraySize) : m_probArray(probArray), m_probArraySize(probArraySize) {
        // Nothing more...
    }
    
    void initialise(uint32_t N, uint32_t K) {
        // Does nothing...
    }
    
    void set_min_max_ploidy(uint32_t min_ploidy, uint32_t max_ploidy, uint32_t min_number_of_entries, uint32_t max_number_of_entries) {
        // Does nothing...
    }
    
    bool set_sample(size_t i) {
        return true;
    }
    
    void set_number_of_entries(uint32_t P, uint32_t Z, genfile::OrderType order_type, genfile::ValueType value_type) {
        // Does nothing...
    }
    
    void set_value(uint32_t i, genfile::MissingValue value) {
        m_probArray[m_currentIndex] = NAN;
        m_currentIndex++;
    }
    
    void set_value(uint32_t i, double value) {
        m_probArray[m_currentIndex] = value;
        m_currentIndex++;
    }
    
    void finalise() {
        if (m_currentIndex != m_probArraySize) {
            stringstream errorMsg;
            errorMsg << "Read " << m_currentIndex << " probabilities, expected " << m_probArraySize << ".";
            throw runtime_error(errorMsg.str());
        }
    }
    
private:
    
    float* m_probArray;
    
    size_t m_probArraySize;
    
    size_t m_currentIndex = 0;
};

BgenParser::BgenParser() {
    // Does nothing...
}
    
void BgenParser::init(string bgenFilePath) {
    
    m_stream.reset(new ifstream(bgenFilePath, ifstream::binary));
    
    if (!*m_stream) {
        stringstream errorMsg;
        errorMsg << "File not found: " << bgenFilePath;
        throw invalid_argument(errorMsg.str());
    }
    
    uint32_t offset;
    genfile::bgen::read_offset(*m_stream, &offset);
    genfile::bgen::read_header_block(*m_stream, &m_context);
        
    nSamples = m_context.number_of_samples;
    nVariants = m_context.number_of_variants;
}

void BgenParser::readVariantProbs(uint64_t variantFileStartPosition, float* probArray) {
    
    m_stream->seekg(variantFileStartPosition);
    
    bool wasSnpReadingSucceessful = genfile::bgen::read_snp_identifying_data(
        *m_stream, m_context, &m_variantInfo.snpid, &m_variantInfo.rsid, &m_variantInfo.chromosome, &m_variantInfo.position,
        [this](size_t n) {m_variantInfo.alleles.resize(n);},
        [this](size_t i, const string& allele) {m_variantInfo.alleles[i] = allele;}
    );
    
    if (!wasSnpReadingSucceessful) {
        stringstream errorMsg;
        errorMsg << "Failed reading variant at: " << variantFileStartPosition;
        throw runtime_error(errorMsg.str());
    }
    
    ProbArraySetter setter(probArray, nSamples * N_PROBS_PER_SAMPLE);
    genfile::bgen::read_and_parse_genotype_data_block(*m_stream, m_context, setter, &m_buffer1, &m_buffer2);
}
