package BULMADependences;

import java.io.Serializable;
import java.util.Map;

public class BulmaOutputGrouping implements Serializable {
	
	private static final long serialVersionUID = -7855076809125995429L;
	private Map<String, BulmaBusteOutput> mapOutputGrouping;

	public BulmaOutputGrouping() {
		super();
	}
	
	public BulmaOutputGrouping(Map<String, BulmaBusteOutput> mapOutputGrouping) {
		this.mapOutputGrouping = mapOutputGrouping;
	}

	public Map<String, BulmaBusteOutput> getMapOutputGrouping() {
		return mapOutputGrouping;
	}

	public void setMapOutputGrouping(Map<String, BulmaBusteOutput> mapOutputGrouping) {
		this.mapOutputGrouping = mapOutputGrouping;
	}

	public boolean containsShapeSequence(String shapeSequence) {
		return mapOutputGrouping.containsKey(shapeSequence);
	}
	
	@Override
	public String toString() {
		return "ShapeID elements grouped by Bulma output: " + this.mapOutputGrouping.size();
	}
}
