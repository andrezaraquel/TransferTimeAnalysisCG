package integration;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Queue;
import java.util.StringTokenizer;
import java.util.concurrent.TimeUnit;

import org.apache.commons.collections.IteratorUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.FlatMapFunction;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.api.java.function.PairFunction;
import org.locationtech.spatial4j.context.jts.JtsSpatialContext;

import com.clearspring.analytics.util.Lists;
import com.vividsolutions.jts.geom.Coordinate;
import com.vividsolutions.jts.geom.GeometryFactory;
import com.vividsolutions.jts.geom.LineString;
import com.vividsolutions.jts.geom.Point;

import BULMADependences.BulmaBusteOutput;
import BULMADependences.BulmaOutputGrouping;
import BULMADependences.GPSLine;
import BULMADependences.GeoLine;
import BULMADependences.OutputString;
import BULMADependences.PossibleShape;
import BULMADependences.PreProcessingBULMAInput;
import BULMADependences.Problem;
import BULMADependences.ShapeLine;
import BULMADependences.Trip;
import PointDependencies.GPSPoint;
import PointDependencies.GeoPoint;
import PointDependencies.ShapePoint;
import scala.Tuple2;

/**
 * 
 * Matching GPS with Shape, i.e., identifying which shape the bus is running (some cities has multiple shapes for the same route).
 * Besides this, matching each gps point with the closest shape point, stop point and separate the trips.
 * At least, matching each stop with shape point and find gps data for it. The output is filtered by stop.
 *
 * @input GPS: bus.code, latitude, longitude, timestamp, line.code, gps.id
 * 		  GTFS: shapes.csv (preprocessed with route)
 *
 * @return route, trip_number/no_shape_code, shape_id/-, route_frequency/-, shape_sequence/-, shape_lat/-, shape_lon/-, 
 *		distance_traveled, bus_code, gps_id, gps_lat, gps_lon, distance_to_shape_point/-, gps_timestamp,  stop_id, trip_problem_code
 */


public class MatchingGPSShapeStop {

	// to separate trips, when no gps point was send
	private static final double THRESHOLD_TIME = 600000; // 20 minutes
	//TODO CG: Some trips are no splitted (has code -3) because no gps was send (interval): 092 - 2042 - trip 7
	
	// threshold to identify outliers and to identify initial and final points based on greater distance and shape points 
	private static final double PERCENTAGE_DISTANCE = 0.09; 
	private static final String FILE_SEPARATOR = ",";
	private static final String SLASH = "/";
	private static final String OUTPUT_HEADER = "route,tripNum,shapeId,routeFrequency,shapeSequence,shapeLat,shapeLon,distanceTraveledShape,"
			+ "busCode,gpsPointId,gpsLat,gpsLon,distanceToShapePoint,gps_datetime,stopPointId,problem";

	public static void main(String[] args) throws IOException, URISyntaxException, ParseException {

		if (args.length < 4) {
			System.err.println(
					"Usage: <shape file> <directory of GPS files> <directory of output path> <number of partitions>\n"
					+ "Ex: CampinaGrande data/gtfs/ data/gps/ data/output/ 1");
			System.exit(1);
		}

		Long initialTime = System.currentTimeMillis();

		String city = args[0];
		String GTFSFilesPath = args[1] + city + "/";
		String GPSFilesPath = args[2] + city + "/";
		String outputPath = args[3] + city + "/";
		String busStopsFile = GTFSFilesPath + "stop_times_shapes.txt";
		int minPartitions = Integer.valueOf(args[4]);

		SparkConf sparkConf = new SparkConf().setAppName("MatchingGPSShapeStop").setMaster("local");
//		SparkConf sparkConf = new SparkConf().setAppName("MatchingGPSShapeStop"); // to run on cluster
		JavaSparkContext context = new JavaSparkContext(sparkConf);

		generateOutputFiles(city, GTFSFilesPath, GPSFilesPath, outputPath, busStopsFile, minPartitions, context);

		context.stop();
		context.close();
		System.out.println("Execution time: " + TimeUnit.MILLISECONDS.toMinutes(System.currentTimeMillis() - initialTime) + " min");
	}

	private static void generateOutputFiles(String city, String pathFileShapes, String pathGPSFiles, String outputPath, String busStopsFile,
			int minPartitions, JavaSparkContext context) throws IOException, URISyntaxException, ParseException {

		Configuration conf = new Configuration();
		FileSystem fs = FileSystem.get(new URI(pathGPSFiles), conf);
		FileStatus[] fileStatus = fs.listStatus(new Path(pathGPSFiles));

		for (FileStatus file : fileStatus) {
			String fileName = file.getPath().getName();
			
			if (!fileName.contains("preprocessed_")) {
				// Standardizing GPS data input, sorting and adding gps id
				PreProcessingBULMAInput.filterGPSData(pathGPSFiles + fileName, city);
				
//				JavaRDD<String> rddOutputBuLMA = executeBULMA(pathFileShapes, pathGPSFiles + "preprocessed_" + file.getPath().getName(), 
//						minPartitions, context, city);
				
				
//				JavaPairRDD<String, Iterable<GeoPoint>> rddOutputBuLMA = executeBULMA(pathFileShapes, pathGPSFilesPreProcessed + file.getPath().getName(),
//						minPartitions, context);

//				rddOutputBuLMA.saveAsTextFile(pathOutput + SLASH
//						+ file.getPath().getName().substring(0, file.getPath().getName().lastIndexOf(".csv")));
				
				// Get the day of analysis. Curitiba data are saved one day after.
				String stringFileDate;
				String correctDate;
				if (city.equals("CampinaGrande")) {
					stringFileDate = fileName.substring(18, fileName.lastIndexOf(".csv"));
					correctDate = stringFileDate;
				} else if (city.equals("Recife")) {
					stringFileDate = fileName.substring(fileName.lastIndexOf("_")+1, fileName.lastIndexOf(".csv"));
					correctDate = stringFileDate;
				} else {
					stringFileDate = subtractDay(fileName.substring(0, fileName.lastIndexOf("_veiculos")));
					correctDate = fileName.substring(fileName.lastIndexOf("_"), fileName.lastIndexOf(".csv"));
				}
				
				JavaRDD<String> rddOutputBuLMABusTE = executeBULMA(pathFileShapes, pathGPSFiles + "preprocessed_" + stringFileDate + ".csv", 
						busStopsFile, correctDate, minPartitions, context, city);

				/**
				 * Inserts a header into each output file
				 * 
				 * @return the output file with a new header
				 */
				Function2<Integer, Iterator<String>, Iterator<String>> insertHeader = new Function2<Integer, Iterator<String>, Iterator<String>>() {

					private static final long serialVersionUID = 6196875196870694185L;

					@SuppressWarnings("unchecked")
					public Iterator<String> call(Integer index, Iterator<String> iterator) throws Exception {
						List<String> output = new LinkedList<String>();
						output.add(OUTPUT_HEADER);
						output.addAll(IteratorUtils.toList(iterator));

						return output.iterator();
					}
				};

				rddOutputBuLMABusTE.mapPartitionsWithIndex(insertHeader, false)
						.saveAsTextFile(outputPath + SLASH + "BuLMABusTE_" + stringFileDate);
				
			}
		}
	}

	@SuppressWarnings("serial")
	private static JavaRDD<String> executeBULMA(String pathFileShapes, String pathGPSFile, String busStopsFile, final String stringDate, int minPartitions,
			JavaSparkContext ctx, final String city) {
		
		Function2<Integer, Iterator<String>, Iterator<String>> removeHeader = new Function2<Integer, Iterator<String>, Iterator<String>>() {

			public Iterator<String> call(Integer index, Iterator<String> iterator) throws Exception {
				if (index == 0 && iterator.hasNext()) {
					iterator.next();
					return iterator;
				} else {
					return iterator;
				}
			}
		};

		JavaRDD<String> gpsString = ctx.textFile(pathGPSFile, minPartitions).mapPartitionsWithIndex(removeHeader,
				false);
		JavaRDD<String> shapeString = ctx.textFile(pathFileShapes + "shapes.csv", minPartitions).mapPartitionsWithIndex(removeHeader,
				false);

		JavaPairRDD<String, Iterable<GeoPoint>> rddGPSPointsPair = gpsString
				.mapToPair(new PairFunction<String, String, GeoPoint>() {

					public Tuple2<String, GeoPoint> call(String s) throws Exception {
						GPSPoint gpsPoint = GPSPoint.createGPSPointWithId(s);

						return new Tuple2<String, GeoPoint>(gpsPoint.getBusCode(), gpsPoint);
					}

				}).groupByKey(minPartitions);

		JavaPairRDD<String, Iterable<GeoPoint>> rddShapePointsPair = shapeString
				.mapToPair(new PairFunction<String, String, GeoPoint>() {

					public Tuple2<String, GeoPoint> call(String s) throws Exception {
						ShapePoint shapePoint = ShapePoint.createShapePointRoute(s);
						return new Tuple2<String, GeoPoint>(shapePoint.getId(), shapePoint);
					}
				}).groupByKey(minPartitions);

		JavaPairRDD<String, Object> rddGPSLinePair = rddGPSPointsPair
				.mapToPair(new PairFunction<Tuple2<String, Iterable<GeoPoint>>, String, Object>() {

					@SuppressWarnings("deprecation")
					GeometryFactory geometryFactory = JtsSpatialContext.GEO.getGeometryFactory();

					public Tuple2<String, Object> call(Tuple2<String, Iterable<GeoPoint>> pair) throws Exception {

						List<Coordinate> coordinates = new ArrayList<Coordinate>();
						Double latitude;
						Double longitude;
						String lineBlockingKey = null;
						float greaterDistance = 0;

						List<GeoPoint> listGeoPoint = Lists.newArrayList(pair._2);
						
						Collections.sort(listGeoPoint);
						
						for (int i = 0; i < listGeoPoint.size(); i++) {
							GeoPoint currentGeoPoint = listGeoPoint.get(i);
							if (i < listGeoPoint.size() - 1) {
								float currentDistance = GeoPoint.getDistanceInMeters(currentGeoPoint,
										listGeoPoint.get(i + 1));
								if (currentDistance > greaterDistance) {
									greaterDistance = currentDistance;
								}
							}

							latitude = Double.valueOf(currentGeoPoint.getLatitude());
							longitude = Double.valueOf(currentGeoPoint.getLongitude());
							coordinates.add(new Coordinate(latitude, longitude));

							if (lineBlockingKey == null && !((GPSPoint) currentGeoPoint).getLineCode().equals("REC")) {
								lineBlockingKey = ((GPSPoint) currentGeoPoint).getLineCode();
							}
						}

						Coordinate[] array = new Coordinate[coordinates.size()];
						GeoLine geoLine = null;
						try {

							if (array.length > 1 && lineBlockingKey != null) {
								LineString lineString = geometryFactory.createLineString(coordinates.toArray(array));
								geoLine = new GPSLine(pair._1, lineString, lineBlockingKey, listGeoPoint,
										greaterDistance);
							} else if (array.length >= 1) {
								geoLine = new GPSLine(pair._1, null, "REC", listGeoPoint, greaterDistance);
							}

						} catch (Exception e) {
							throw new Exception("LineString cannot be created. " + e);
						}

						return new Tuple2<String, Object>(lineBlockingKey, geoLine);
					}
				});

		
		// Grouping ShapeLine by route
		JavaPairRDD<String, Object> rddShapeLinePairRoute = rddShapePointsPair
				.mapToPair(new PairFunction<Tuple2<String, Iterable<GeoPoint>>, String, Object>() {

					@SuppressWarnings("deprecation")
					GeometryFactory geometryFactory = JtsSpatialContext.GEO.getGeometryFactory();

					public Tuple2<String, Object> call(Tuple2<String, Iterable<GeoPoint>> pair) throws Exception {

						List<Coordinate> coordinates = new ArrayList<Coordinate>();
						Double latitude;
						Double longitude;
						ShapePoint lastPoint = null;
						String lineBlockingKey = null;
						float greaterDistance = 0;

						List<GeoPoint> listGeoPoint = Lists.newArrayList(pair._2);
						Collections.sort(listGeoPoint);
						
						for (int i = 0; i < listGeoPoint.size(); i++) {
							GeoPoint currentGeoPoint = listGeoPoint.get(i);
							if (i < listGeoPoint.size() - 1) {
								float currentDistance = GeoPoint.getDistanceInMeters(currentGeoPoint,
										listGeoPoint.get(i + 1));
								if (currentDistance > greaterDistance) {
									greaterDistance = currentDistance;
								}
							}

							latitude = Double.valueOf(currentGeoPoint.getLatitude());
							longitude = Double.valueOf(currentGeoPoint.getLongitude());
							coordinates.add(new Coordinate(latitude, longitude));
							lastPoint = (ShapePoint) currentGeoPoint;

							if (lineBlockingKey == null) {
								lineBlockingKey = ((ShapePoint) currentGeoPoint).getRoute();
							}
						}

						Coordinate[] array = new Coordinate[coordinates.size()];

						LineString lineString = geometryFactory.createLineString(coordinates.toArray(array));
						Float distanceTraveled = lastPoint.getDistanceTraveled();
						String route = lastPoint.getRoute();
						GeoLine geoLine = new ShapeLine(pair._1, lineString, distanceTraveled, lineBlockingKey,
								listGeoPoint, route, greaterDistance);

						return new Tuple2<String, Object>(lineBlockingKey, geoLine);
					}
				});

		JavaPairRDD<String, Iterable<Object>> rddGroupedUnionLines = rddGPSLinePair.union(rddShapeLinePairRoute)
				.groupByKey(minPartitions);
		

		JavaRDD<Tuple2<GPSLine, List<PossibleShape>>> rddPossibleShapes = rddGroupedUnionLines.flatMap(
				new FlatMapFunction<Tuple2<String, Iterable<Object>>, Tuple2<GPSLine, List<PossibleShape>>>() {

					public Iterator<Tuple2<GPSLine, List<PossibleShape>>> call(Tuple2<String, Iterable<Object>> entry)
							throws Exception {

						List<ShapeLine> shapeLineList = new ArrayList<ShapeLine>();
						List<GPSLine> gpsLineList = new ArrayList<GPSLine>();

						List<Tuple2<GPSLine, List<PossibleShape>>> listOutput = new LinkedList<Tuple2<GPSLine, List<PossibleShape>>>();

						Iterator<Object> iteratorGeoLine = entry._2.iterator();
						GeoLine geoLine;
						while (iteratorGeoLine.hasNext()) {
							geoLine = (GeoLine) iteratorGeoLine.next();

							if (geoLine instanceof ShapeLine) {
								shapeLineList.add((ShapeLine) geoLine);
							} else if (geoLine != null) {
								gpsLineList.add((GPSLine) geoLine);
							}
						}

						PossibleShape possibleShape;
						GPSPoint firstPointGPS;
						long timePreviousPointGPS;
						String blockingKeyFromTime = null;
						GPSPoint currentPoint;
						float currentDistanceToStartPoint;
						float currentDistanceToEndPoint;
						int thresholdDistanceCurrentShape = 0;

						while (!gpsLineList.isEmpty()) {
							GPSLine gpsLine = gpsLineList.remove(0);

							List<PossibleShape> listPossibleShapes = new LinkedList<PossibleShape>();
							for (ShapeLine shapeLine : shapeLineList) {
								
								thresholdDistanceCurrentShape = (int) (shapeLine.getDistanceTraveled()
										/ (shapeLine.getListGeoPoints().size() * PERCENTAGE_DISTANCE));
								
								shapeLine.setThresholdDistance(thresholdDistanceCurrentShape);
								
								blockingKeyFromTime = null;
								possibleShape = new PossibleShape(gpsLine.getListGeoPoints(), shapeLine);
								firstPointGPS = (GPSPoint) gpsLine.getListGeoPoints().get(0);

								for (int i = 0; i < gpsLine.getListGeoPoints().size(); i++) {
									GPSPoint auxPoint = (GPSPoint) gpsLine.getListGeoPoints().get(i);
									if (!auxPoint.getLineCode().equals("REC")) {
										firstPointGPS = auxPoint;
										break;
									}
								}

								timePreviousPointGPS = firstPointGPS.getTime();
								int lastIndexFirst = -2;
								int lastIndexEnd = -2;
								for (int i = 0; i < gpsLine.getListGeoPoints().size(); i++) {
									currentPoint = (GPSPoint) gpsLine.getListGeoPoints().get(i);

									if (!currentPoint.getLineCode().equals("REC")) {
										currentDistanceToStartPoint = possibleShape
												.getDistanceInMetersToStartPointShape(currentPoint);
										currentDistanceToEndPoint = possibleShape
												.getDistanceInMetersToEndPointShape(currentPoint);

										if (currentDistanceToStartPoint < thresholdDistanceCurrentShape) {

											if (blockingKeyFromTime == null
													|| currentPoint.getTime() - timePreviousPointGPS > THRESHOLD_TIME) {
												if (i > lastIndexFirst + 1) {
													blockingKeyFromTime = currentPoint.getBlockingKeyFromTime();
												}
												lastIndexFirst = i;
											}
											timePreviousPointGPS = currentPoint.getTime();
											possibleShape.addPossibleFirstPoint(
													new Tuple2<String, Integer>(blockingKeyFromTime, i));

										} else if (currentDistanceToEndPoint < thresholdDistanceCurrentShape) {

											if (blockingKeyFromTime == null
													|| currentPoint.getTime() - timePreviousPointGPS > THRESHOLD_TIME) {
												if (i > lastIndexEnd + 1) {
													blockingKeyFromTime = currentPoint.getBlockingKeyFromTime();
												}
												lastIndexEnd = i;
											}

											timePreviousPointGPS = currentPoint.getTime();

											if (possibleShape.isRoundShape()) {
												possibleShape.addPossibleFirstPoint(
														new Tuple2<String, Integer>(blockingKeyFromTime, i));
											} else {
												possibleShape.addPossibleLastPoint(
														new Tuple2<String, Integer>(blockingKeyFromTime, i));
											}

										}
									}
								}
								listPossibleShapes.add(possibleShape);

						
							}
							listOutput.add(new Tuple2<GPSLine, List<PossibleShape>>(gpsLine, listPossibleShapes));
						}

						return listOutput.iterator();
					}
				});

		JavaRDD<Tuple2<GPSLine, List<PossibleShape>>> rddTrueShapes = rddPossibleShapes
				.map(new Function<Tuple2<GPSLine, List<PossibleShape>>, Tuple2<GPSLine, List<PossibleShape>>>() {

					public Tuple2<GPSLine, List<PossibleShape>> call(Tuple2<GPSLine, List<PossibleShape>> entry)
							throws Exception {

						Queue<Tuple2<String, Integer>> firstGPSPoints;
						Queue<Tuple2<String, Integer>> lastGPSPoints;

						Map<GPSLine, List<PossibleShape>> mapOutput = new HashMap<GPSLine, List<PossibleShape>>();

						boolean hasRoundShape = false;

						List<PossibleShape> possibleShapesList = entry._2;
						GPSLine gpsLine = entry._1;

						for (PossibleShape possibleShape : possibleShapesList) {
							if (possibleShape.isRoundShape()) {
								hasRoundShape = true;
							}

							firstGPSPoints = possibleShape.getFirstGPSPoints();
							lastGPSPoints = possibleShape.getLastGPSPoints();

							if (firstGPSPoints.size() >= 2 && lastGPSPoints.isEmpty()) {

								possibleShape.addFirstAndLastPoint(firstGPSPoints.poll()._2);

								Integer indexPoint;
								while (firstGPSPoints.size() >= 2) {
									indexPoint = firstGPSPoints.poll()._2;
									possibleShape.addFirstAndLastPoint(indexPoint);
									possibleShape.addFirstAndLastPoint(indexPoint + 1);
								}
								possibleShape.addFirstAndLastPoint(firstGPSPoints.poll()._2);

							} else if (firstGPSPoints.isEmpty() && lastGPSPoints.size() >= 2) {

								possibleShape.addFirstAndLastPoint(lastGPSPoints.poll()._2);

								Integer indexPoint;
								while (lastGPSPoints.size() >= 2) {
									indexPoint = lastGPSPoints.poll()._2;
									possibleShape.addFirstAndLastPoint(indexPoint);
									possibleShape.addFirstAndLastPoint(indexPoint + 1);
								}
								possibleShape.addFirstAndLastPoint(lastGPSPoints.poll()._2);

							} else {

								int previousLastPointPosition = 0;
								boolean isFirstTrip = true;
								while (!firstGPSPoints.isEmpty() && !lastGPSPoints.isEmpty()) {

									int firstPointPosition = firstGPSPoints.poll()._2;
									if (isFirstTrip || firstPointPosition > previousLastPointPosition) {

										while (!lastGPSPoints.isEmpty()) {
											int lastPointPosition = lastGPSPoints.poll()._2;

											if (firstPointPosition < lastPointPosition) {

												possibleShape.addFirstAndLastPoint(firstPointPosition);
												possibleShape.addFirstAndLastPoint(lastPointPosition);
												previousLastPointPosition = lastPointPosition;

												break;

											} else if (!isFirstTrip) {
												possibleShape.addFirstAndLastPoint(previousLastPointPosition * -1);
												possibleShape.addFirstAndLastPoint(lastPointPosition * -1);
											}
										}
									} else if (!isFirstTrip) {

										Integer notProblem = possibleShape.getListIndexFirstAndLastGPSPoints()
												.remove(possibleShape.getListIndexFirstAndLastGPSPoints().size() - 1);
										Integer problem = possibleShape.getListIndexFirstAndLastGPSPoints()
												.remove(possibleShape.getListIndexFirstAndLastGPSPoints().size() - 1);

										possibleShape.addFirstAndLastPoint(problem * -1);
										possibleShape.addFirstAndLastPoint(firstPointPosition * -1);
										possibleShape.addFirstAndLastPoint(firstPointPosition + 1);
										possibleShape.addFirstAndLastPoint(notProblem);
									}

									isFirstTrip = false;
								}
							}

						}
						Collections.sort(possibleShapesList);
						if (!hasRoundShape && possibleShapesList.size() > 2) {
							
							Integer indexSmaller = null;
							Integer indexSmaller2 = null;
							Integer numberPoints1 = null;
							Integer numberPoints2 = null;
							PossibleShape possibleShape1 = null;
							PossibleShape possibleShape2 = null;

							for (PossibleShape possibleShape : possibleShapesList) {
								if (possibleShape.getListIndexFirstAndLastGPSPoints().size() > 2) {
									int value = Math.abs(possibleShape.getListIndexFirstAndLastGPSPoints().get(0));
									int value2 = Math.abs(possibleShape.getListIndexFirstAndLastGPSPoints().get(1));

									int difference = value2 - value;

									if (indexSmaller == null || value < indexSmaller) {

										indexSmaller2 = indexSmaller;
										possibleShape2 = possibleShape1;
										numberPoints2 = numberPoints1;
										indexSmaller = value;
										possibleShape1 = possibleShape;
										numberPoints1 = difference;

									} else if (indexSmaller2 == null || value < indexSmaller2) {
										indexSmaller2 = value;
										possibleShape2 = possibleShape;
										numberPoints2 = difference;
									}
								}

							}

							if (numberPoints1 != null && numberPoints2 != null && numberPoints1 > numberPoints2) {
								possibleShapesList = findComplementaryShape(possibleShape1, possibleShapesList);
							} else if (numberPoints1 != null && numberPoints2 != null) {
								possibleShapesList = findComplementaryShape(possibleShape2, possibleShapesList);
							}

						} else if (hasRoundShape && possibleShapesList.size() > 1) {

							PossibleShape bestShape = null;
							Long timeFirstPoint = null;
							Integer numberPoints = null;

							for (PossibleShape possibleShape : possibleShapesList) {

								if (possibleShape.getListIndexFirstAndLastGPSPoints().size() >= 1) {
									GPSPoint firstPointCurrentPossibleShape = ((GPSPoint) possibleShape
											.getListGPSPoints()
											.get(Math.abs(possibleShape.getListIndexFirstAndLastGPSPoints().get(0))));

									if (timeFirstPoint == null
											|| firstPointCurrentPossibleShape.getTime() < timeFirstPoint) {
										timeFirstPoint = firstPointCurrentPossibleShape.getTime();
										bestShape = possibleShape;
										numberPoints = possibleShape.getListIndexFirstAndLastGPSPoints().get(1)
												- possibleShape.getListIndexFirstAndLastGPSPoints().get(0);

									} else if (firstPointCurrentPossibleShape.getTime() == timeFirstPoint
											&& (possibleShape.getListIndexFirstAndLastGPSPoints().get(1) - possibleShape
													.getListIndexFirstAndLastGPSPoints().get(0)) > numberPoints) {
										bestShape = possibleShape;
										numberPoints = possibleShape.getListIndexFirstAndLastGPSPoints().get(1)
												- possibleShape.getListIndexFirstAndLastGPSPoints().get(0);
									}
								}
							}

							List<PossibleShape> possibleShapeCurrentGPS = new ArrayList<PossibleShape>();
							possibleShapeCurrentGPS.add(bestShape);
							possibleShapesList = possibleShapeCurrentGPS;
						}

						mapOutput.put(gpsLine, possibleShapesList);
						return new Tuple2<GPSLine, List<PossibleShape>>(gpsLine, possibleShapesList);
					}

					private List<PossibleShape> findComplementaryShape(PossibleShape entryShape,
							List<PossibleShape> possibleShapes) {
						PossibleShape complementaryShape = null;
						Point firstPointEntryShape = entryShape.getShapeLine().getLine().getStartPoint();
						Point endPointEntryShape = entryShape.getShapeLine().getLine().getEndPoint();

						for (PossibleShape possibleShape : possibleShapes) {
							Point currentStartPoint = possibleShape.getShapeLine().getLine().getStartPoint();
							Point currentEndPoint = possibleShape.getShapeLine().getLine().getEndPoint();

							if (GeoPoint.getDistanceInMeters(firstPointEntryShape, currentEndPoint) < possibleShape
									.getShapeLine().getGreaterDistancePoints()
									&& GeoPoint.getDistanceInMeters(endPointEntryShape,
											currentStartPoint) < possibleShape.getShapeLine()
													.getGreaterDistancePoints()) {
								complementaryShape = possibleShape;
								break;
							}

						}

						List<PossibleShape> newList = new ArrayList<PossibleShape>();
						newList.add(entryShape);
						newList.add(complementaryShape);

						return newList;
					}
				});

		JavaRDD<Tuple2<GPSLine, Map<Integer, List<Trip>>>> rddTrips = rddTrueShapes
				.map(new Function<Tuple2<GPSLine, List<PossibleShape>>, Tuple2<GPSLine, Map<Integer, List<Trip>>>>() {

					public Tuple2<GPSLine, Map<Integer, List<Trip>>> call(Tuple2<GPSLine, List<PossibleShape>> entry)
							throws Exception {

						Map<GPSLine, Map<Integer, List<Trip>>> mapOutput = new HashMap<GPSLine, Map<Integer, List<Trip>>>();

						GPSLine gpsLine = entry._1;
						List<PossibleShape> possibleShapesList = entry._2();
						Map<Integer, List<Trip>> mapTrips = new HashMap<Integer, List<Trip>>();

						for (PossibleShape possibleShape : possibleShapesList) {
							if (possibleShape != null) {
								int numberTrip = 1;

								for (int i = 0; i < possibleShape.getListIndexFirstAndLastGPSPoints().size()
										- 1; i += 2) {
									boolean isTripProblem = false;
									int firstIndex = possibleShape.getListIndexFirstAndLastGPSPoints().get(i);
									int lastIndex = possibleShape.getListIndexFirstAndLastGPSPoints().get(i + 1);

									if (lastIndex < 0) {
										isTripProblem = true;
										firstIndex *= -1;
										lastIndex *= -1;
									}

									if (isTripProblem) {
										addTrip(gpsLine.getListGeoPoints(), mapTrips, numberTrip++, firstIndex,
												lastIndex, possibleShape.getShapeLine(), Problem.TRIP_PROBLEM);
									} else {
										addTrip(gpsLine.getListGeoPoints(), mapTrips, numberTrip++, firstIndex,
												lastIndex, possibleShape.getShapeLine(), Problem.NO_PROBLEM);
									}

								}
							}
						}

						setUpOutliers(gpsLine.getListGeoPoints(), mapTrips);

						mapOutput.put(gpsLine, mapTrips);

						return new Tuple2<GPSLine, Map<Integer, List<Trip>>>(gpsLine, mapTrips);
					}

					private void setUpOutliers(List<GeoPoint> listGeoPoints, Map<Integer, List<Trip>> mapTrips) {

						for (int i = 1; i <= mapTrips.keySet().size(); i++) {

							List<Trip> currentlistTrip = mapTrips.get(i);

							if (!currentlistTrip.isEmpty()) {

								ArrayList<GeoPoint> pointsTripGPS;
								int currentLastIndex = currentlistTrip.get(currentlistTrip.size() - 1).getLastIndex();

								if (i == 1 && !currentlistTrip.isEmpty()) {
									int currentFirstIndex = currentlistTrip.get(0).getFirstIndex();
									if (currentFirstIndex > 0) {
										pointsTripGPS = new ArrayList<GeoPoint>();
										pointsTripGPS.addAll(listGeoPoints.subList(0, currentFirstIndex));
										try {
											currentlistTrip.add(0,
													new Trip(null, pointsTripGPS, Problem.OUTLIER_POINT));
										} catch (Exception e) {
											e.printStackTrace();
										}
									}
									
								} else if (i > 1 && i == mapTrips.keySet().size()) {
									if (listGeoPoints.size() - 1 > currentLastIndex) {

										pointsTripGPS = new ArrayList<GeoPoint>();
										pointsTripGPS.addAll(
												listGeoPoints.subList(currentLastIndex + 1, listGeoPoints.size()));
										try {
											currentlistTrip.add(new Trip(null, pointsTripGPS, Problem.OUTLIER_POINT));
										} catch (Exception e) {
											e.printStackTrace();
										}
									}

								} else if (i > 1) {
									List<Trip> nextListTrip = mapTrips.get(i + 1);
									if (!nextListTrip.isEmpty()) {
										int nextFirstIndex = nextListTrip.get(0).getFirstIndex();
										if (nextFirstIndex > currentLastIndex + 1) {

											pointsTripGPS = new ArrayList<GeoPoint>();
											pointsTripGPS.addAll(
													listGeoPoints.subList(currentLastIndex + 1, nextFirstIndex));

											try {
												currentlistTrip
														.add(new Trip(null, pointsTripGPS, Problem.OUTLIER_POINT));
											} catch (Exception e) {
												e.printStackTrace();
											}
										}
									}
								}
							}
							mapTrips.put(i, currentlistTrip);
						}
					}

					private void addTrip(List<GeoPoint> listGeoPoints, Map<Integer, List<Trip>> mapTrips,
							Integer numberTrip, Integer firstIndex, Integer lastIndex, ShapeLine shapeLine,
							Problem problem) {

						if (numberTrip > 1) {
							List<Trip> previousTrip = mapTrips.get(numberTrip - 1);
							if (!previousTrip.isEmpty()) {
								int lastIndexPreviousTrip = previousTrip.get(previousTrip.size() - 1).getLastIndex()
										+ 1;
								if (firstIndex < lastIndexPreviousTrip) {
									firstIndex = lastIndexPreviousTrip;
								}
							}
						}

						if (numberTrip < mapTrips.keySet().size()) {
							List<Trip> nextTrip = mapTrips.get(numberTrip + 1);
							if (!nextTrip.isEmpty()) {
								int firstIndexNextTrip = nextTrip.get(0).getFirstIndex();
								if (lastIndex >= firstIndexNextTrip) {
									lastIndex = firstIndexNextTrip;
								}
							}
						}

						if (!mapTrips.containsKey(numberTrip)) {
							mapTrips.put(numberTrip, new ArrayList<Trip>());
						}

						List<Trip> listTrips = mapTrips.get(numberTrip);
						ArrayList<GeoPoint> pointsTripGPS;
						Trip newTrip = null;

						if (!listTrips.isEmpty()) {
							int indexPreviousLastPoint = listTrips.get(listTrips.size() - 1).getLastIndex() + 1;
							if (firstIndex > indexPreviousLastPoint) {

								pointsTripGPS = new ArrayList<GeoPoint>();
								pointsTripGPS.addAll(listGeoPoints.subList(indexPreviousLastPoint, firstIndex));

								try {
									newTrip = new Trip(null, pointsTripGPS, Problem.OUTLIER_POINT);
									newTrip.setFirstIndex(indexPreviousLastPoint);
									newTrip.setLastIndex(firstIndex);
									listTrips.add(newTrip);
								} catch (Exception e) {
									e.printStackTrace();
								}
							} else if (firstIndex < indexPreviousLastPoint) {
								firstIndex = indexPreviousLastPoint;
							}
						}

						if (firstIndex < lastIndex) { 
							pointsTripGPS = new ArrayList<GeoPoint>();
							pointsTripGPS.addAll(listGeoPoints.subList(firstIndex, lastIndex + 1));

							try {
								newTrip = new Trip(shapeLine, pointsTripGPS, problem);
								newTrip.setFirstIndex(firstIndex);
								newTrip.setLastIndex(lastIndex);
								listTrips.add(newTrip);
								
							} catch (Exception e) {
								e.printStackTrace();
							}
						}
						mapTrips.put(numberTrip, listTrips);
					}

				});

		JavaRDD<Tuple2<GPSLine, Map<Integer, List<Trip>>>> rddClosestPoint = rddTrips.map(
				new Function<Tuple2<GPSLine, Map<Integer, List<Trip>>>, Tuple2<GPSLine, Map<Integer, List<Trip>>>>() {

					public Tuple2<GPSLine, Map<Integer, List<Trip>>> call(
							Tuple2<GPSLine, Map<Integer, List<Trip>>> entry) throws Exception {


						GPSLine gpsLine = entry._1;
						Map<Integer, List<Trip>> mapTrips = entry._2;

						for (int numberTrip = 1; numberTrip <= mapTrips.size(); numberTrip++) {

							for (Trip trip : mapTrips.get(numberTrip)) {
								if (trip.getShapeLine() != null) {
									for (GeoPoint gpsPoint : trip.getGpsPoints()) {

										GeoPoint closestPoint = trip.getShapePoints().get(0);
										float distanceClosestPoint = GeoPoint.getDistanceInMeters(gpsPoint,
												closestPoint);

										for (GeoPoint currentShapePoint : trip.getShapePoints()) {
											float currentDistance = GeoPoint.getDistanceInMeters(gpsPoint,
													currentShapePoint);

											if (currentDistance <= distanceClosestPoint) {
												distanceClosestPoint = currentDistance;
												closestPoint = currentShapePoint;
											}
										}

										((GPSPoint) gpsPoint).setClosestPoint(closestPoint);
										((GPSPoint) gpsPoint).setNumberTrip(numberTrip);
										((GPSPoint) gpsPoint).setDistanceClosestShapePoint(distanceClosestPoint);
										((GPSPoint) gpsPoint)
												.setThresholdShape(trip.getShapeLine().getThresholdDistance());
									}
								}
							}
						}

						return new Tuple2<GPSLine, Map<Integer, List<Trip>>>(gpsLine, mapTrips);
					}
				});

		JavaRDD<String> rddBulmaOutput = rddClosestPoint
				.flatMap(new FlatMapFunction<Tuple2<GPSLine, Map<Integer, List<Trip>>>, String>() {

					public Iterator<String> call(Tuple2<GPSLine, Map<Integer, List<Trip>>> entry) throws Exception {

						List<String> listOutput = new ArrayList<String>();

						GPSLine gpsLine = entry._1;
						Map<Integer, List<Trip>> mapTrips = entry._2;

						if (gpsLine != null) {

							if (mapTrips.isEmpty()) {
								GPSPoint gpsPoint;
								for (GeoPoint geoPoint : gpsLine.getListGeoPoints()) {
									String stringOutput = "";
									
									gpsPoint = (GPSPoint) geoPoint;
									stringOutput += Problem.NO_SHAPE.getCode() + FILE_SEPARATOR;
									stringOutput += gpsPoint.getLineCode() + FILE_SEPARATOR;

									stringOutput += "-" + FILE_SEPARATOR;
									stringOutput += "-" + FILE_SEPARATOR;
									stringOutput += "-" + FILE_SEPARATOR;
									stringOutput += "-" + FILE_SEPARATOR;
									stringOutput += "-" + FILE_SEPARATOR;

									stringOutput += gpsPoint.getGpsId() + FILE_SEPARATOR;
									stringOutput += gpsPoint.getBusCode() + FILE_SEPARATOR;
									stringOutput += gpsPoint.getTimeStamp() + FILE_SEPARATOR;
									stringOutput += gpsPoint.getLatitude() + FILE_SEPARATOR;
									stringOutput += gpsPoint.getLongitude() + FILE_SEPARATOR;

									stringOutput += "-" + FILE_SEPARATOR;
									stringOutput += "-" + FILE_SEPARATOR;

									stringOutput += Problem.NO_SHAPE.getCode();
									listOutput.add(stringOutput);

								}
							}

							for (Integer key : mapTrips.keySet()) {
								for (Trip trip : mapTrips.get(key)) {

									for (GeoPoint geoPoint : trip.getGPSPoints()) {

										GPSPoint gpsPoint = (GPSPoint) geoPoint;
										String stringOutput = "";
										stringOutput += key + FILE_SEPARATOR;
										stringOutput += gpsPoint.getLineCode() + FILE_SEPARATOR;
										if (trip.getShapeLine() == null) {
											stringOutput += "-" + FILE_SEPARATOR;
											stringOutput += "-" + FILE_SEPARATOR;
											stringOutput += "-" + FILE_SEPARATOR;
											stringOutput += "-" + FILE_SEPARATOR;
											stringOutput += "-" + FILE_SEPARATOR;
										} else {
											stringOutput += gpsPoint.getClosestPoint().getId() + FILE_SEPARATOR;
											stringOutput += gpsPoint.getClosestPoint().getRouteFrequency() + FILE_SEPARATOR;
											stringOutput += gpsPoint.getClosestPoint().getPointSequence()
													+ FILE_SEPARATOR;
											stringOutput += gpsPoint.getClosestPoint().getLatitude() + FILE_SEPARATOR;
											stringOutput += gpsPoint.getClosestPoint().getLongitude() + FILE_SEPARATOR;
										}

										stringOutput += gpsPoint.getGpsId() + FILE_SEPARATOR;
										stringOutput += gpsPoint.getBusCode() + FILE_SEPARATOR;
										stringOutput += gpsPoint.getTimeStamp() + FILE_SEPARATOR;
										stringOutput += gpsPoint.getLatitude() + FILE_SEPARATOR;
										stringOutput += gpsPoint.getLongitude() + FILE_SEPARATOR;

										if (trip.getShapeLine() == null) {
											stringOutput += "-" + FILE_SEPARATOR;
											stringOutput += "-" + FILE_SEPARATOR;
										} else {
											stringOutput += gpsPoint.getDistanceClosestShapePoint() + FILE_SEPARATOR;
											stringOutput += gpsPoint.getThresholdShape() + FILE_SEPARATOR;
										}

										if (trip.getProblem().equals(Problem.TRIP_PROBLEM)) {
											stringOutput += trip.getProblem().getCode();
										} else if (gpsPoint.getDistanceClosestShapePoint() > gpsPoint
												.getThresholdShape()) {
											stringOutput += Problem.OUTLIER_POINT.getCode();
										} else {
											stringOutput += trip.getProblem().getCode();
										}
										listOutput.add(stringOutput);
									}
								}
							}
						}

						return listOutput.iterator();
					}
				});

		//----------------End of GPS point - Shape point integration----------------
		
		
		//----------------Begin of GPS point - Shape point - Stop point integration----------------
		
		JavaRDD<String> busStopsString = ctx.textFile(busStopsFile, minPartitions)
				.mapPartitionsWithIndex(removeHeader, false);
		
		
		JavaPairRDD<String, Object> rddBusStops = busStopsString.mapToPair(new PairFunction<String, String, Object>() {

			public Tuple2<String, Object> call(String busStopsString) throws Exception {
				String[] splittedEntry = busStopsString.split(FILE_SEPARATOR);
				// shapeID , shapeSequence + '.' + stopId
				return new Tuple2<String, Object>(splittedEntry[7], splittedEntry[8] + "." + splittedEntry[2]);
			}
		});
		
		
		// Grouping BULMA output by busCode-tripNum-shapeID
		JavaPairRDD<String, Iterable<BulmaBusteOutput>> rddBulmaOutputGrouped = rddBulmaOutput
				.mapToPair(new PairFunction<String, String, BulmaBusteOutput>() {

					public Tuple2<String, BulmaBusteOutput> call(String bulmaOutputString) throws Exception {
						StringTokenizer st = new StringTokenizer(bulmaOutputString, FILE_SEPARATOR);
						
						BulmaBusteOutput bulmaOutput = new BulmaBusteOutput(st.nextToken(), st.nextToken(), st.nextToken(), 
								st.nextToken(), st.nextToken(), st.nextToken(), st.nextToken(), st.nextToken(), 
								st.nextToken(), st.nextToken(), st.nextToken(), st.nextToken(), st.nextToken(), 
								st.nextToken(), st.nextToken(), stringDate);
						
						String codeTripShapeKey = bulmaOutput.getBusCode() + ":" + bulmaOutput.getTripNum() + ":"
								+ bulmaOutput.getShapeId();

						return new Tuple2<String, BulmaBusteOutput>(codeTripShapeKey, bulmaOutput);
					}
				}).groupByKey(minPartitions);
		
		
		// Grouping all BULMA output that has the same shapeID
		JavaPairRDD<String, Object> rddBulmaOutputGrouping = rddBulmaOutputGrouped
				.mapToPair(new PairFunction<Tuple2<String, Iterable<BulmaBusteOutput>>, String, Object>() {

					public Tuple2<String, Object> call(Tuple2<String, Iterable<BulmaBusteOutput>> codeTripShape_BulmaOutput) throws Exception {
						Map<String, BulmaBusteOutput> mapOutputGrouping = new HashMap<String, BulmaBusteOutput>();
						String codeTripShapeKey = codeTripShape_BulmaOutput._1.split("\\:")[2]; // [2] = shapeId
									
						List<BulmaBusteOutput> listBulmaOutput = Lists.newArrayList(codeTripShape_BulmaOutput._2);
						Collections.sort(listBulmaOutput);
						
						for (BulmaBusteOutput bulmaOutput : listBulmaOutput) {
							mapOutputGrouping.put(bulmaOutput.getShapeSequence(), bulmaOutput);
						}

						return new Tuple2<String, Object>(codeTripShapeKey, new BulmaOutputGrouping(mapOutputGrouping));
					}
				});
		
		// Grouping ShapeLine by shapeID
		JavaPairRDD<String, Object> rddShapeLinePairID = rddShapePointsPair
				.mapToPair(new PairFunction<Tuple2<String, Iterable<GeoPoint>>, String, Object>() {

					public Tuple2<String, Object> call(Tuple2<String, Iterable<GeoPoint>> shapeId_shapePointList) throws Exception {

						LinkedList<GeoPoint> listShapePoints = new LinkedList<GeoPoint>();
						Iterator<GeoPoint> it = shapeId_shapePointList._2.iterator();
						while (it.hasNext()) {
							listShapePoints.add(it.next());
						}
												
						Collections.sort(listShapePoints);

						String route = ((ShapePoint) listShapePoints.get(listShapePoints.size() - 1)).getRoute();
						ShapeLine shapeLine = new ShapeLine(shapeId_shapePointList._1, listShapePoints, route);

						return new Tuple2<String, Object>(shapeId_shapePointList._1, shapeLine);
					}
				});

		
		// Union of BULMA output, Shape and Stops by shapeID
		JavaPairRDD<String, Iterable<Object>> rddBulmaShapeStopUnion = rddBulmaOutputGrouping.union(rddShapeLinePairID)
				.union(rddBusStops).groupByKey(minPartitions);
		
		JavaRDD<String> rddInterpolation = rddBulmaShapeStopUnion
				.flatMap(new FlatMapFunction<Tuple2<String, Iterable<Object>>, String>() {

					private ShapeLine shapeLine;
					private List<BulmaOutputGrouping> listBulmaOutputGrouping;
					private Map<String, String> mapStopPoints; // Map<ShapeSequence,StopPointId>
					private Map<String, String> mapAux;

					public Iterator<String> call(Tuple2<String, Iterable<Object>> shapeId_objects) throws Exception {
						List<String> listOutput = new LinkedList<String>();

						shapeLine = null;
						listBulmaOutputGrouping = new ArrayList<BulmaOutputGrouping>();
						mapStopPoints = new HashMap<String, String>();
						mapAux = new HashMap<String, String>();

						List<Object> listInput = Lists.newArrayList(shapeId_objects._2);
						for (Object obj : listInput) {
							if (obj instanceof BulmaOutputGrouping) {
								listBulmaOutputGrouping.add((BulmaOutputGrouping) obj);
							} else if (obj instanceof ShapeLine) {
								if (shapeLine != null) {
									System.err.println("Error: multiple shapes for the same shapeID.");
								}
								shapeLine = (ShapeLine) obj;
							} else {
								String shapeSequenceStopId = (String) obj;
								String[] splittedObj = shapeSequenceStopId.split("\\.");

								mapStopPoints.put(splittedObj[0], splittedObj[1]); //shapeSequence - StopID
								mapAux.put(splittedObj[0], splittedObj[1]);
							}
						}

						if (shapeLine == null) {
							return listOutput.iterator();
						}

						for (BulmaOutputGrouping bulmaOutputGrouping : listBulmaOutputGrouping) {
							Tuple2<Float, String> previousPoint = null;
							Tuple2<Float, String> nextPoint = null;
							List<Integer> pointsBetweenGPS = new LinkedList<Integer>();

							String tripNum = "-";

							for (int i = 0; i < shapeLine.getListGeoPoints().size(); i++) {
								ShapePoint currentShapePoint = (ShapePoint) shapeLine.getListGeoPoints().get(i);
								String currentShapeSequence = currentShapePoint.getPointSequence();
								String currentDistanceTraveled = currentShapePoint.getDistanceTraveled().toString();
								String currentShapeId = shapeLine.getId(); // shape id
								String currentLatShape = currentShapePoint.getLatitude();
								String currentLonShape = currentShapePoint.getLongitude();
								String currentRoute = shapeLine.getRoute();
								String currentRouteFrequency = currentShapePoint.getRouteFrequency();

								String currentTimestamp;
								String currentGPSDateTime;

								if (previousPoint == null) {
									if (bulmaOutputGrouping.containsShapeSequence(currentShapeSequence)) {

										BulmaBusteOutput currentOutput = bulmaOutputGrouping.getMapOutputGrouping()
												.get(currentShapeSequence);

										currentTimestamp = currentOutput.getTimestamp();
										currentGPSDateTime = currentOutput.getGps_datetime();
										
										previousPoint = new Tuple2<Float, String>(
												currentShapePoint.getDistanceTraveled(), currentTimestamp);

										String busCode = currentOutput.getBusCode();
										String gpsPointId = currentOutput.getGpsPointId();
										String problemCode = currentOutput.getTripProblem();
										tripNum = currentOutput.getTripNum();
										String latGPS = currentOutput.getLatGPS();
										String lonGPS = currentOutput.getLonGPS();
										String distanceToShape = currentOutput.getDistance();

										addOutput(currentRoute, tripNum, currentShapeId, currentRouteFrequency, currentShapeSequence,
												currentLatShape, currentLonShape, currentDistanceTraveled, busCode,
												gpsPointId, latGPS, lonGPS, distanceToShape, currentGPSDateTime,
												problemCode, listOutput);

									} else { //when there is no gps point for this shape point
										addOutput(currentRoute, tripNum, currentShapeId, currentRouteFrequency, currentShapeSequence,
												currentLatShape, currentLonShape, currentDistanceTraveled, "-", "-",
												"-", "-", "-", "-", "-", listOutput);
									}
								} else {

									if (bulmaOutputGrouping.containsShapeSequence(currentShapeSequence)) {
										BulmaBusteOutput currentOutput = bulmaOutputGrouping.getMapOutputGrouping()
												.get(currentShapeSequence);

										String busCode = currentOutput.getBusCode();
										String gpsPointId = currentOutput.getGpsPointId();
										String problemCode = currentOutput.getTripProblem();
										tripNum = currentOutput.getTripNum();
										String latGPS = currentOutput.getLatGPS();
										String lonGPS = currentOutput.getLonGPS();
										String distanceToShape = currentOutput.getDistance();
										currentTimestamp = currentOutput.getTimestamp();
										currentGPSDateTime = currentOutput.getGps_datetime();

										nextPoint = new Tuple2<Float, String>(
												currentShapePoint.getDistanceTraveled(), currentTimestamp);

										generateOutputFromPointsInBetween(currentShapeId, tripNum, previousPoint,
												pointsBetweenGPS, nextPoint, shapeLine.getListGeoPoints(), busCode,
												listOutput, stringDate);

										addOutput(currentRoute, tripNum, currentShapeId, currentRouteFrequency, currentShapeSequence,
												currentLatShape, currentLonShape, currentDistanceTraveled, busCode,
												gpsPointId, latGPS, lonGPS, distanceToShape, currentGPSDateTime,
												problemCode, listOutput);

										previousPoint = nextPoint;
										nextPoint = null;
										pointsBetweenGPS = new LinkedList<Integer>();

									} else {
										pointsBetweenGPS.add(i);
									}
								}
							}

							if (!pointsBetweenGPS.isEmpty()) { //shape points between gps or shape line without gps point
								for (Integer indexPointInBetween : pointsBetweenGPS) {

									ShapePoint currentShapePoint = (ShapePoint) shapeLine.getListGeoPoints()
											.get(indexPointInBetween);
									String currentShapeSequence = currentShapePoint.getPointSequence();
									String currentDistanceTraveled = currentShapePoint.getDistanceTraveled().toString();
									String currentShapeId = shapeLine.getId();
									String currentRouteFrequency = currentShapePoint.getRouteFrequency();

									String currentLatShape = currentShapePoint.getLatitude();
									String currentLonShape = currentShapePoint.getLongitude();
									String currentRoute = shapeLine.getRoute();

									addOutput(currentRoute, tripNum, currentShapeId, currentRouteFrequency, currentShapeSequence,
											currentLatShape, currentLonShape, currentDistanceTraveled, "-", "-", "-",
											"-", "-", "-", "-", listOutput);
								}
							}
						}

						return listOutput.iterator();
					}

					// Add to the output just the gps-shape which corresponds to some stop point 
					private void addOutput(String route, String tripNum, String shapeId, String routeFrequency, String shapeSequence,
							String shapeLat, String shapeLon, String distanceTraveledShape, String busCode,
							String gpsPointId, String gpsLat, String gpsLon, String distanceToShapePoint,
							String gps_date_time, String problemCode, List<String> listOutput) {

						String stopPointId = mapStopPoints.get(shapeSequence);
						mapAux.remove(shapeSequence);
						
						if (stopPointId != null) { // filter only stops
							String problem;

							try {
								problem = Problem.getById(Integer.valueOf(problemCode));
							} catch (Exception e) {
								problem = "BETWEEN";
							}

							String outputString = route + FILE_SEPARATOR + tripNum + FILE_SEPARATOR + shapeId + FILE_SEPARATOR
									+ routeFrequency + FILE_SEPARATOR + shapeSequence + FILE_SEPARATOR + shapeLat + FILE_SEPARATOR + 
									shapeLon + FILE_SEPARATOR + distanceTraveledShape + FILE_SEPARATOR + busCode + FILE_SEPARATOR + 
									gpsPointId + FILE_SEPARATOR + gpsLat + FILE_SEPARATOR + gpsLon + FILE_SEPARATOR + distanceToShapePoint + 
									FILE_SEPARATOR + gps_date_time + FILE_SEPARATOR + stopPointId + FILE_SEPARATOR + problem;

							listOutput.add(outputString);
						}
					}

					private void generateOutputFromPointsInBetween(String shapeId, String tripNum,
							Tuple2<Float, String> previousGPSPoint, List<Integer> pointsBetweenGPS,
							Tuple2<Float, String> nextGPSPoint, List<GeoPoint> listGeoPointsShape, String busCode,
							List<String> listOutput, String previousDate) throws ParseException {

						Float previousDistanceTraveled = previousGPSPoint._1;
						long previousTime = getTimeLong(previousGPSPoint._2);
						Float nextDistanceTraveled = nextGPSPoint._1;
						long nextTime = getTimeLong(nextGPSPoint._2);
						Float distanceTraveled = nextDistanceTraveled - previousDistanceTraveled;
						long time = nextTime - previousTime;
						String gpsDateTime;

						Float currentDistanceTraveled;
						long generatedTimeDifference;
						long generatedTime;
						String generatedTimeString;
						String sequence;
						String routeFrequency;
						String distance;
						String latShape;
						String lonShape;
						String route;
						for (Integer indexPointsInBetween : pointsBetweenGPS) {

							currentDistanceTraveled = ((ShapePoint) listGeoPointsShape.get(indexPointsInBetween)).getDistanceTraveled()
									- previousDistanceTraveled;
							generatedTimeDifference = (long) ((currentDistanceTraveled * time) / distanceTraveled);
							generatedTime = previousTime + generatedTimeDifference;
							generatedTimeString = getTimeString(generatedTime);
							gpsDateTime = previousDate + " " + generatedTimeString;
							sequence = ((ShapePoint) listGeoPointsShape.get(indexPointsInBetween)).getPointSequence();
							routeFrequency = ((ShapePoint) listGeoPointsShape.get(indexPointsInBetween)).getRouteFrequency();
							latShape = listGeoPointsShape.get(indexPointsInBetween).getLatitude();
							lonShape = listGeoPointsShape.get(indexPointsInBetween).getLongitude();
							route = ((ShapePoint) listGeoPointsShape.get(indexPointsInBetween)).getRoute();
							distance = ((ShapePoint) listGeoPointsShape.get(indexPointsInBetween)).getDistanceTraveled().toString();

							addOutput(route, tripNum, shapeId, routeFrequency, sequence, latShape, lonShape, distance, busCode, "-",
									"-", "-", "-", gpsDateTime, "-", listOutput);
						}
					}

					private String getTimeString(long generatedTime) {
						Date date = new Date(generatedTime);
						DateFormat formatter = new SimpleDateFormat("HH:mm:ss");
						return formatter.format(date);
					}

					private long getTimeLong(String timestamp) throws ParseException {
						SimpleDateFormat parser = new SimpleDateFormat("HH:mm:ss");
						return parser.parse(timestamp).getTime();
					}
				});
		
		
		// Grouping interpolation by Bus Code
		JavaPairRDD<String, Iterable<OutputString>> rddMapInterpolation = rddInterpolation
				.mapToPair(new PairFunction<String, String, OutputString>() {

					public Tuple2<String, OutputString> call(String stringOutput) throws Exception {
						String[] splittedEntry = stringOutput.split(FILE_SEPARATOR);
						OutputString str = new OutputString(stringOutput);
						
						return new Tuple2<String, OutputString>(splittedEntry[8], str);
					}
				}).groupByKey();
		
//		route, trip_number/no_shape_code, shape_id/-, route_frequency/-, shape_sequence/-, shape_lat/-, shape_lon/-, 
//		distance_traveled, bus_code, gps_id, gps_lat, gps_lon, distance_to_shape_point/-, gps_timestamp,  stop_id, trip_problem_code
		
		// Sorting the output by timestamp
		JavaRDD<String> rddBulmaBusteOutput = rddMapInterpolation
				.flatMap(new FlatMapFunction<Tuple2<String,Iterable<OutputString>>, String>() {

					public Iterator<String> call(Tuple2<String, Iterable<OutputString>> busCode_stringOutput) throws Exception {

						List<String> listOutput = new LinkedList<String>();
						List<OutputString> OutputList = Lists.newArrayList(busCode_stringOutput._2);									
						
						Collections.sort(OutputList);
												
						String nextTimeString = null;
						for (int i = OutputList.size() - 1; i >= 0; i--) {
							String currentString = OutputList.get(i).getOutputString();
							String currentBusStop = currentString.split(FILE_SEPARATOR)[14];

							if (!currentBusStop.equals("-")) {
								String currentTimeString = currentString.split(FILE_SEPARATOR)[13];
								if (!currentTimeString.equals("-")) {
									currentTimeString = currentTimeString.split(" ")[1];
									
									if (nextTimeString == null) {
										nextTimeString = currentTimeString;
										listOutput.add(0, currentString);

									} else {
										listOutput.add(0, currentString);
										nextTimeString = currentTimeString;
									}
									
								} else {									
									listOutput.add(0, currentString);
								}
							}
						}

						return listOutput.iterator();
					}
				});

		// return each gps point per stop
		return rddBulmaBusteOutput;
	}
	
	/**
	 * Gets the previous date based on date passed as parameter
	 * 
	 * @param stringDate
	 * 	The current date
	 * @return
	 * 	The previous date
	 * @throws ParseException
	 */
	public static String subtractDay(String stringDate) throws ParseException {

		DateFormat targetFormat = new SimpleDateFormat("yyyy_MM_dd", Locale.ENGLISH);
		Date date = targetFormat.parse(stringDate);
		
	    Calendar cal = Calendar.getInstance();
	    cal.setTime(date);
	    cal.add(Calendar.DAY_OF_MONTH, -1);
	    
	    DateFormat originalFormat = new SimpleDateFormat("EEE MMM dd kk:mm:ss z yyyy", Locale.ENGLISH);
	    Date newDate = originalFormat.parse(cal.getTime().toString());
	    String formattedDate = targetFormat.format(newDate).replace("_", "-"); 
	    
	    return formattedDate;
	}
}