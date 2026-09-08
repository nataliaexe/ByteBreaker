"""
Tests for ByteBreaker Modules
"""
import pytest
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.recon import ReconX
from modules.scanner import VulnScan
from modules.cracker import HashCrack
from modules.forensics import ForensicKit
from core.config import Config
from core.logger import ByteBreakerLogger


@pytest.fixture
def config():
    """Create test configuration"""
    return Config()


@pytest.fixture
def logger(tmp_path):
    """Create test logger"""
    return ByteBreakerLogger("TestLogger", str(tmp_path))


class TestReconX:
    """Test reconnaissance module"""
    
    def test_init(self, config, logger):
        """Test ReconX initialization"""
        recon = ReconX(config, logger)
        assert recon is not None
        assert recon.config == config
    
    def test_is_ip(self, config, logger):
        """Test IP validation"""
        recon = ReconX(config, logger)
        assert recon._is_ip("192.168.1.1") == True
        assert recon._is_ip("example.com") == False
    
    @pytest.mark.asyncio
    async def test_basic_info(self, config, logger):
        """Test basic info gathering"""
        recon = ReconX(config, logger)
        result = await recon.get_basic_info("127.0.0.1")
        assert "ip_addresses" in result
        assert result["is_ip"] == True


class TestVulnScan:
    """Test vulnerability scanner module"""
    
    def test_init(self, config, logger):
        """Test VulnScan initialization"""
        scanner = VulnScan(config, logger)
        assert scanner is not None
        assert scanner.vulnerabilities == []
    
    @pytest.mark.asyncio
    async def test_scan_network(self, config, logger):
        """Test network vulnerability scan"""
        scanner = VulnScan(config, logger)
        await scanner._scan_network_vulnerabilities("127.0.0.1")
        # Should not crash


class TestHashCrack:
    """Test hash cracking module"""
    
    def test_init(self, config, logger):
        """Test HashCrack initialization"""
        cracker = HashCrack(config, logger)
        assert cracker is not None
        assert "password" in cracker.common_passwords
    
    def test_validate_hash(self, config, logger):
        """Test hash validation"""
        cracker = HashCrack(config, logger)
        assert cracker._validate_hash("5f4dcc3b5aa765d61d8327deb882cf99", "md5") == True
        assert cracker._validate_hash("invalid", "md5") == False
    
    def test_calculate_hash(self, config, logger):
        """Test hash calculation"""
        cracker = HashCrack(config, logger)
        import hashlib
        expected = hashlib.md5("password".encode()).hexdigest()
        assert cracker._calculate_hash("password", "md5") == expected
    
    @pytest.mark.asyncio
    async def test_crack_password(self, config, logger):
        """Test password cracking"""
        cracker = HashCrack(config, logger)
        import hashlib
        hash_value = hashlib.md5("password".encode()).hexdigest()
        result = await cracker.crack(hash_value, "md5")
        assert result["success"] == True
        assert result["password"] == "password"


class TestForensicKit:
    """Test forensics module"""
    
    def test_init(self, config, logger):
        """Test ForensicKit initialization"""
        forensics = ForensicKit(config, logger)
        assert forensics is not None
        assert "application/pdf" in forensics.file_types
    
    @pytest.mark.asyncio
    async def test_analyze_nonexistent_file(self, config, logger, tmp_path):
        """Test analyzing non-existent file"""
        forensics = ForensicKit(config, logger)
        with pytest.raises(FileNotFoundError):
            await forensics.analyze(str(tmp_path / "nonexistent.txt"))
    
    @pytest.mark.asyncio
    async def test_analyze_file(self, config, logger, tmp_path):
        """Test analyzing a file"""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")
        
        forensics = ForensicKit(config, logger)
        result = await forensics.analyze(str(test_file), "full")
        assert "hashes" in result
        assert "md5" in result["hashes"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
