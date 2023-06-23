#ifndef QTUMUTILS_H
#define QTUMUTILS_H

#include <libdevcore/Common.h>
#include <libdevcore/FixedHash.h>

/**
 * qtumutils Provides utility functions to EVM for functionalities that already exist in qtum
 */
namespace qtumutils
{
/**
 * @brief btc_ecrecover Wrapper to CPubKey::RecoverCompact
 */
bool btc_ecrecover(dev::h256 const& hash, dev::u256 const& v, dev::h256 const& r, dev::h256 const& s, dev::h256 & key);


/**
 * @brief The ChainIdType enum Chain Id values for the networks
 */
enum ChainIdType
{
    MAINNET = 81,
    TESTNET = 8889,
    REGTEST = 8890,
};

/**
 * @brief eth_getChainId Get eth chain id
 * @param blockHeight Block height
 * @param shanghaiHeight Shanghai fork height
 * @return chain id
 */
int eth_getChainId(int blockHeight, int shanghaiHeight);

/**
 * @brief eth_getChainId Get eth chain id and cache it
 * @param blockHeight Block height
 * @return chain id
 */
int eth_getChainId(int blockHeight);

}

#endif
