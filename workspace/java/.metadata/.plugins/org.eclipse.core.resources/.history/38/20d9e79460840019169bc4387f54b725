package BULMADependences;

import java.io.Serializable;

public class BulmaBusteOutput implements Serializable, Comparable<BulmaBusteOutput> {
	
	private static final long serialVersionUID = 3518929651995019131L;
	private String tripNum;
	private String route;
	private String shapeId;
	private String routeFrequency;
	private String shapeSequence;
	private String latShape;
	private String lonShape;
	private String gpsPointId;
	private String busCode;
	private String timestamp;
	private String latGPS;
	private String lonGPS;
	private String distanceTraveled;
	private String thresholdProblem;
	private String tripProblem;
	private String gps_datetime;
	private String stopID;
	private String distanceToShapePoint;
	private long headway;
	private String nextBusCode;
	private boolean busBunching;
	
	public BulmaBusteOutput() {
		super();
	}
	
//	trip_number,route,shape_id,route_frequency,shape_sequence,shape_lat,shape_lon,
//	gps_id,bus_code,gps_timestamp,gps_lat,gps_lon,distance_to_shape_point,threshold_distance,trip_problem_code
	public BulmaBusteOutput(String tripNum, String route, String shapeId, String routeFrequency, String shapeSequence, String latShape,
			String lonShape, String gpsPointId, String busCode, String timestamp, String latGPS, String lonGPS,
			String distance, String thresholdProblem, String tripProblem, String gps_date) {
		
		this.tripNum = tripNum;
		this.route = route;
		this.shapeId = shapeId;
		this.routeFrequency = routeFrequency;
		this.shapeSequence = shapeSequence;
		this.latShape = latShape;
		this.lonShape = lonShape;
		this.gpsPointId = gpsPointId;
		this.busCode = busCode;
		this.timestamp = timestamp;
		this.latGPS = latGPS;
		this.lonGPS = lonGPS;
		this.distanceTraveled = distance;
		this.thresholdProblem = thresholdProblem;
		this.tripProblem = tripProblem;
		this.gps_datetime = gps_date + " " + timestamp;
	}
	
//	route, trip_number/no_shape_code, shape_id/-, route_frequency/-, shape_sequence/-, shape_lat/-, shape_lon/-, 
//	distance_traveled, bus_code, gps_id, gps_lat, gps_lon, distance_to_shape_point/-, gps_timestamp,  stop_id, trip_problem_code
	public BulmaBusteOutput(String route, String tripNum, String shapeId, String routeFrequency, String shapeSequence, String latShape,
			String lonShape, String distanceTraveled, String busCode, String gpsPointId, String latGPS, String lonGPS, String
			distanceToShapePoint, String timestamp, String stopID, String tripProblem, String aux) {
		
		this.tripNum = tripNum;
		this.route = route;
		this.shapeId = shapeId;
		this.routeFrequency = routeFrequency;
		this.shapeSequence = shapeSequence;
		this.latShape = latShape;
		this.lonShape = lonShape;
		this.gpsPointId = gpsPointId;
		this.busCode = busCode;
		this.timestamp = timestamp.split(" ")[1];
		this.latGPS = latGPS;
		this.lonGPS = lonGPS;
		this.distanceTraveled = distanceTraveled;
		this.tripProblem = tripProblem;
		this.gps_datetime = timestamp; // date and time
		this.stopID = stopID;
		this.distanceToShapePoint = distanceToShapePoint;
	}

	public String getTripNum() {
		return tripNum;
	}

	public void setTripNum(String tripNum) {
		this.tripNum = tripNum;
	}

	public String getRoute() {
		return route;
	}

	public void setRoute(String route) {
		this.route = route;
	}

	public String getShapeId() {
		return shapeId;
	}

	public void setShapeId(String shapeId) {
		this.shapeId = shapeId;
	}

	public String getShapeSequence() {
		return shapeSequence;
	}

	public void setShapeSequence(String shapeSequence) {
		this.shapeSequence = shapeSequence;
	}

	public String getLatShape() {
		return latShape;
	}

	public void setLatShape(String latShape) {
		this.latShape = latShape;
	}

	public String getLonShape() {
		return lonShape;
	}

	public void setLonShape(String lonShape) {
		this.lonShape = lonShape;
	}

	public String getGpsPointId() {
		return gpsPointId;
	}

	public void setGpsPointId(String gpsPointId) {
		this.gpsPointId = gpsPointId;
	}

	public String getBusCode() {
		return busCode;
	}

	public void setBusCode(String busCode) {
		this.busCode = busCode;
	}

	public String getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(String timestamp) {
		this.timestamp = timestamp;
	}

	public String getLatGPS() {
		return latGPS;
	}

	public void setLatGPS(String latGPS) {
		this.latGPS = latGPS;
	}

	public String getLonGPS() {
		return lonGPS;
	}

	public void setLonGPS(String lonGPS) {
		this.lonGPS = lonGPS;
	}

	public String getDistance() {
		return distanceTraveled;
	}

	public void setDinstance(String dinstance) {
		this.distanceTraveled = dinstance;
	}

	public String getThresholdProblem() {
		return thresholdProblem;
	}

	public void setThresholdProblem(String thresholdProblem) {
		this.thresholdProblem = thresholdProblem;
	}

	public String getTripProblem() {
		return tripProblem;
	}

	public void setTripProblem(String tripProblem) {
		this.tripProblem = tripProblem;
	}
	
	public String getGps_datetime() {
		return gps_datetime;
	}

	public void setGps_datetime(String gps_datetime) {
		this.gps_datetime = gps_datetime;
	}
	
	@Override
	public String toString() {
		return tripNum + "," + route + "," + shapeId + ","
				+ shapeSequence + "," + latShape + "," + lonShape + "," + gpsPointId
				+ "," + busCode + "," + timestamp + "," + latGPS + "," + lonGPS
				+ "," + distanceTraveled + "," + thresholdProblem + "," + tripProblem;
	}	
	
	@Override
	public int compareTo(BulmaBusteOutput otherOutput) {
		if (Integer.parseInt(this.timestamp.replaceAll(":", "")) < Integer.parseInt(otherOutput.timestamp.replaceAll(":", ""))) {
            return -1;
        }
        if (Integer.parseInt(this.timestamp.replaceAll(":", "")) > Integer.parseInt(otherOutput.timestamp.replaceAll(":", ""))) {
            return 1;
        }
        return 0;
	}

	public String getRouteFrequency() {
		return routeFrequency;
	}

	public void setRouteFrequency(String routeFrequency) {
		this.routeFrequency = routeFrequency;
	}

	public String getStopID() {
		return stopID;
	}

	public void setStopID(String stopID) {
		this.stopID = stopID;
	}

	public String getDistanceToShapePoint() {
		return distanceToShapePoint;
	}

	public void setDistanceToShapePoint(String distanceToShapePoint) {
		this.distanceToShapePoint = distanceToShapePoint;
	}

	public String getNextBusCode() {
		return nextBusCode;
	}

	public void setNextBusCode(String nextBusCode) {
		this.nextBusCode = nextBusCode;
	}

	public long getHeadway() {
		return headway;
	}

	public void setHeadway(long headway) {
		this.headway = headway;
	}

	public boolean isBusBunching() {
		return busBunching;
	}

	public void setBusBunching(boolean busBunching) {
		this.busBunching = busBunching;
	}
}
