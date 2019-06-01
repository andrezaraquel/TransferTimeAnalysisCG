package BULMADependences;

import java.io.Serializable;

public class OutputString implements Serializable, Comparable<OutputString>{

	private static final long serialVersionUID = 1L;
	private static final String SEPARATOR = ",";
	private String outputString;
	
	// Matching GPS - Shape - Stop
	private String tripNum;
	private String route;
	private String shapeId;
	private String routeFrequency;
	private String shapeSequence;
	private Double latShape;
	private Double lonShape;
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
	
	// Matching GPS - Shape - Stop - Weather
	private Double precipitation;
	private String precipitationTime;
	
	// Matching  GPS - Shape - Stop - Weather - Alert
	private AlertData alertData;
	
	// Matching  GPS - Shape - Stop - Weather - Alert - Jam
	private JamData jamData;
	
	// Matching  GPS - Shape - Stop - Weather - Alert - Jam - Headway - Bus Bunching
	private long headway;
	private String nextBusCode;
	private boolean busBunching;
	
	//	route, trip_number/no_shape_code, shape_id/-, route_frequency/-, shape_sequence/-, shape_lat/-, shape_lon/-, 
//	distance_traveled, bus_code, gps_id, gps_lat, gps_lon, distance_to_shape_point/-, gps_timestamp,  stop_id, trip_problem_code
//	Matching GPS-Shape-Stop output
	public OutputString(String route, String tripNum, String shapeId, String routeFrequency, String shapeSequence, String latShape,
			String lonShape, String distanceTraveled, String busCode, String gpsPointId, String latGPS, String lonGPS, String
			distanceToShapePoint, String timestamp, String stopID, String tripProblem) {
		
		this.tripNum = tripNum;
		this.route = route;
		this.shapeId = shapeId;
		this.routeFrequency = routeFrequency;
		this.shapeSequence = shapeSequence;
		this.latShape = Double.valueOf(latShape);
		this.lonShape = Double.valueOf(lonShape);
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
	
//	Constructor of integrated data for headway labeled
	public OutputString(String route, String tripNum, String shapeId, String routeFrequency, String shapeSequence, String latShape,
			String lonShape, String distanceTraveled, String busCode, String gpsPointId, String latGPS, String lonGPS, String
			distanceToShapePoint, String timestamp, String stopID, String tripProblem, AlertData alertData, JamData jamData) {
		
		this.tripNum = tripNum;
		this.route = route;
		this.shapeId = shapeId;
		this.routeFrequency = routeFrequency;
		this.shapeSequence = shapeSequence;
		this.latShape = Double.valueOf(latShape);
		this.lonShape = Double.valueOf(lonShape);
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
		this.alertData = alertData;
		this.jamData = jamData;
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

	public Double getLatShape() {
		return latShape;
	}

	public void setLatShape(Double latShape) {
		this.latShape = latShape;
	}

	public Double getLonShape() {
		return lonShape;
	}

	public void setLonShape(Double lonShape) {
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
	
	public Double getPrecipitation() {
		return precipitation;
	}

	public void setPrecipitation(Double precipitation) {
		this.precipitation = precipitation;
	}

	public String getPrecipitationTime() {
		return precipitationTime;
	}

	public void setPrecipitationTime(String precipitationTime) {
		this.precipitationTime = precipitationTime;
	}
	
	public AlertData getAlertData() {
		return alertData;
	}

	public void setAlertData(AlertData alertData) {
		this.alertData = alertData;
	}

	public JamData getJamData() {
		return jamData;
	}

	public void setJamData(JamData jamData) {
		this.jamData = jamData;
	}
	
	public OutputString(String outputString) {		
		this.outputString = outputString;
	}	

	public String getOutputString() {
		return outputString;
	}

	public void setOutputString(String outputString) {
		this.outputString = outputString;
	}

	public String getTimestampField() {
		String timestamp;
		if (this.gps_datetime.equals("-")) {
			timestamp = "0";
		} else {
			timestamp = this.gps_datetime.split(" ")[1];
		}
		return timestamp.replaceAll(":", "");
	}

	@Override
	public int compareTo(OutputString otherOut) {
		
		if (Integer.parseInt(this.getTimestampField()) < Integer.parseInt(otherOut.getTimestampField())) {
            return -1;
        }
        if (Integer.parseInt(this.getTimestampField()) > Integer.parseInt(otherOut.getTimestampField())) {
            return 1;
        }
        return 0;
	}

	@Override
	public String toString() {
		return "OutputString [tripNum=" + tripNum + ", route=" + route + ", shapeId=" + shapeId + ", routeFrequency="
				+ routeFrequency + ", shapeSequence=" + shapeSequence + ", latShape=" + latShape + ", lonShape="
				+ lonShape + ", gpsPointId=" + gpsPointId + ", busCode=" + busCode + ", timestamp=" + timestamp
				+ ", latGPS=" + latGPS + ", lonGPS=" + lonGPS + ", distanceTraveled=" + distanceTraveled
				+ ", thresholdProblem=" + thresholdProblem + ", tripProblem=" + tripProblem + ", gps_datetime="
				+ gps_datetime + ", stopID=" + stopID + ", distanceToShapePoint=" + distanceToShapePoint
				+ ", precipitation=" + precipitation + ", precipitationTime=" + precipitationTime + ", alertData="
				+ alertData + ", jamData=" + jamData + ", headway=" + headway + ", nextBusCode=" + nextBusCode
				+ ", busBunching=" + busBunching + "]";
	}
	
	public String getLabeledIntegratedDataString() {
		return getIntegratedOutputString() + SEPARATOR + this.getHeadway() + SEPARATOR + this.isBusBunching() + 
				SEPARATOR + this.getNextBusCode();
	}
	
	public String getIntegratedOutputString() {
		// Sometimes there are no jam or alert for the gps
		String alertDataString = "-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-";
		if (alertData != null) {
			alertDataString = alertData.getDataString();
		}
		
		String jamDataString = "-,-,-,-,-,-,-,-,-";
		if (jamData != null) {
			jamDataString = jamData.getDataString();
		}
		
		return this.getRoute() + SEPARATOR + this.getTripNum() + SEPARATOR + this.getShapeId() + SEPARATOR + 
				this.getRouteFrequency() + SEPARATOR + this.getShapeSequence() + SEPARATOR + this.getLatShape() +
				SEPARATOR + this.getLonShape() + SEPARATOR + this.getDistance() + SEPARATOR + this.getBusCode() + 
				SEPARATOR + this.getGpsPointId() + SEPARATOR + this.getLatGPS() + SEPARATOR + this.getLonGPS() + 
				SEPARATOR + this.getDistanceToShapePoint() + SEPARATOR + this.getGps_datetime() + SEPARATOR + 
				this.getStopID() + SEPARATOR + this.getTripProblem() + SEPARATOR + alertDataString + SEPARATOR +
				jamDataString;
	}
}
