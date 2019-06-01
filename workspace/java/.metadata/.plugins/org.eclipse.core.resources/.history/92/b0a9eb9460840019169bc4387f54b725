package BULMADependences;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import com.vividsolutions.jts.geom.LineString;
import PointDependencies.GeoPoint;

public class GeoLine implements Serializable {
	
	private static final long serialVersionUID = 1L;
	
	private String id;
	private LineString line;
	private String blockingKey;
	private List<GeoPoint> listGeoPoints;
	private float greaterDistancePoints;

	public GeoLine(String id, LineString line, String blockingKey) {
		this.id = id;
		this.line = line;
		this.blockingKey = blockingKey;
		this.listGeoPoints = new ArrayList<GeoPoint>();
	}	
	
	public GeoLine(String id, LineString line, String blockingKey, List<GeoPoint> listGeoPoints, float greaterDistancePoints) {
		this(id, line, blockingKey);
		this.listGeoPoints = listGeoPoints;
		this.greaterDistancePoints = greaterDistancePoints;
	}
	
	public GeoLine(String id, LinkedList<GeoPoint> listGeoPoint, String route) {
		this.id = id;
		this.listGeoPoints = listGeoPoint;
		this.blockingKey = route;
	}
	
	public String getId() {
		return this.id;
	}

	public void setId(String id) {
		this.id = id;
	}	
	
	public LineString getLine() {
		return this.line;
	}

	public void setLine(LineString line) {
		this.line = line;
	}

	public String getBlockingKey() {
		return this.blockingKey;
	}

	public void setBlockingKey(String blockingKey) {
		this.blockingKey = blockingKey;
	}

	public List<GeoPoint> getListGeoPoints() {
		return this.listGeoPoints;
	}
	
	public GeoPoint getFirstPoint() {
		if (listGeoPoints.size() == 0) {
			return null;
		}
		return this.listGeoPoints.get(0);
	}
	
	public GeoPoint getLastPoint() {
		if (listGeoPoints.size() == 0) {
			return null;
		}
		return this.listGeoPoints.get(listGeoPoints.size() -1);
	}

	public void setListGeoPoints(List<GeoPoint> listGeoPoints) {
		this.listGeoPoints = listGeoPoints;
	}
	
	public float getGreaterDistancePoints() {
		return greaterDistancePoints;
	}

	public void setGreaterDistancePoints(float greaterDistancePoints) {
		this.greaterDistancePoints = greaterDistancePoints;
	}

	@Override
	public String toString() {
		return "GeoLine [id=" + id + ", blockingKey=" + blockingKey + ", listGeoPoints_size="
				+ listGeoPoints.size() + "]";
	}
}