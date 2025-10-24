from typing import List
from domain_objects import Recommendation

class OutputGenerator:
    def write_recommendations(self, recommendations: List[Recommendation], filename='output.txt'):
        """Writes the final sorted recommendations to a file."""
        with open(filename, 'w') as f:
            for rec in recommendations:
                f.write(f"{rec.recommended_artist.name}: {rec.total_weight:.4f}\n")

    def write_roots(self, recommendations: List[Recommendation], filename='outroot.txt'):
        """Writes the contributing artists (roots) for each recommendation."""
        # Sort by artist name for consistent output
        sorted_recs = sorted(recommendations, key=lambda r: r.recommended_artist.name)
        with open(filename, 'w') as f:
            for rec in sorted_recs:
                root_info = ", ".join(
                    f"{aw.artist.name} ({aw.weight:.4f})" for aw in rec.contributing_artists
                )
                f.write(f"{rec.recommended_artist.name} -> from: [{root_info}]\n")