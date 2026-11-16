"""EIS-KKA-REF-001: platform-independent mathematical reference models."""
from .activation import kka_activation
from .detector import BalancedDetector, DetectorOutput
from .transfer import ComplexTransfer, apply_complex_transfer, complex_transfer
from .interference import balanced_cross_term, total_intensity
__all__ = ["BalancedDetector", "ComplexTransfer", "DetectorOutput", "apply_complex_transfer", "balanced_cross_term", "complex_transfer", "kka_activation", "total_intensity"]
