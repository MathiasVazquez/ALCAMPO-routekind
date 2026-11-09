import leaflet from "leaflet"
import { ref, computed, nextTick } from 'vue'
import { useLocation } from "src/context"

const distanceBetween = (lat1, lng1, lat2, lng2) => {
  const toRad = (value) => value * Math.PI / 180

  const R = 6371 // km
  const dLat = toRad(lat2-lat1)
  const dLng = toRad(lng2-lng1)
  const lat1Rad = toRad(lat1)
  const lat2Rad = toRad(lat2)

  const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.sin(dLng/2) * Math.sin(dLng/2) * Math.cos(lat1Rad) * Math.cos(lat2Rad)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  const kmDistance = Math.round((R * c + Number.EPSILON) * 10) / 10
  const mtDistance = Math.round((R * c * 1000) + Number.EPSILON)
  return {
    label: kmDistance < 1 ? `${mtDistance} metros` : `${kmDistance} Km`,
    unit: kmDistance < 1 ? 'metros' : 'Km',
    Km: kmDistance,
    metros: mtDistance,
  }
}

const defineCurve = () => {

  L.Curve = L.Path.extend({
      options: {
      },

      initialize: function (path, options) {
          L.setOptions(this, options);
          this._setPath(path);
      },

      // Added to follow the naming convention of L.Polyline and other Leaflet component classes:
      // (https://leafletjs.com/reference-1.6.0.html#polyline-setlatlngs)
      setLatLngs: function (path) {
          return this.setPath(path);
      },

      getLatLngs: function () {
          return this.getPath();
      },

      _updateBounds: function () {
          var tolerance = this._clickTolerance();
          var tolerancePoint = new L.Point(tolerance, tolerance);

          //_pxBounds is critical for canvas renderer, used to determine area that needs redrawing
          this._pxBounds = new L.Bounds([
              this._rawPxBounds.min.subtract(tolerancePoint),
              this._rawPxBounds.max.add(tolerancePoint)
          ]);
      },

      getPath: function () {
          return this._coords;
      },

      setPath: function (path) {
          this._setPath(path);
          return this.redraw();
      },

      getBounds: function () {
          return this._bounds;
      },

      _setPath: function (path) {
          this._coords = path;
          this._bounds = this._computeBounds();
      },

      _computeBounds: function () {
          var bound = new L.LatLngBounds();
          var lastPoint;
          var lastCommand;
          var coord;
          for (var i = 0; i < this._coords.length; i++) {
              coord = this._coords[i];
              if (typeof coord == 'string' || coord instanceof String) {
                  lastCommand = coord;
              } else if (lastCommand == 'H') {
                  bound.extend([lastPoint.lat, coord[0]]);
                  lastPoint = new L.latLng(lastPoint.lat, coord[0]);
              } else if (lastCommand == 'V') {
                  bound.extend([coord[0], lastPoint.lng]);
                  lastPoint = new L.latLng(coord[0], lastPoint.lng);
              } else if (lastCommand == 'C') {
                  var controlPoint1 = new L.latLng(coord[0], coord[1]);
                  coord = this._coords[++i];
                  var controlPoint2 = new L.latLng(coord[0], coord[1]);
                  coord = this._coords[++i];
                  var endPoint = new L.latLng(coord[0], coord[1]);

                  bound.extend(controlPoint1);
                  bound.extend(controlPoint2);
                  bound.extend(endPoint);

                  endPoint.controlPoint1 = controlPoint1;
                  endPoint.controlPoint2 = controlPoint2;
                  lastPoint = endPoint;
              } else if (lastCommand == 'S') {
                  var controlPoint2 = new L.latLng(coord[0], coord[1]);
                  coord = this._coords[++i];
                  var endPoint = new L.latLng(coord[0], coord[1]);

                  var controlPoint1 = lastPoint;
                  if (lastPoint.controlPoint2) {
                      var diffLat = lastPoint.lat - lastPoint.controlPoint2.lat;
                      var diffLng = lastPoint.lng - lastPoint.controlPoint2.lng;
                      controlPoint1 = new L.latLng(lastPoint.lat + diffLat, lastPoint.lng + diffLng);
                  }

                  bound.extend(controlPoint1);
                  bound.extend(controlPoint2);
                  bound.extend(endPoint);

                  endPoint.controlPoint1 = controlPoint1;
                  endPoint.controlPoint2 = controlPoint2;
                  lastPoint = endPoint;
              } else if (lastCommand == 'Q') {
                  var controlPoint = new L.latLng(coord[0], coord[1]);
                  coord = this._coords[++i];
                  var endPoint = new L.latLng(coord[0], coord[1]);

                  bound.extend(controlPoint);
                  bound.extend(endPoint);

                  endPoint.controlPoint = controlPoint;
                  lastPoint = endPoint;
              } else if (lastCommand == 'T') {
                  var endPoint = new L.latLng(coord[0], coord[1]);

                  var controlPoint = lastPoint;
                  if (lastPoint.controlPoint) {
                      var diffLat = lastPoint.lat - lastPoint.controlPoint.lat;
                      var diffLng = lastPoint.lng - lastPoint.controlPoint.lng;
                      controlPoint = new L.latLng(lastPoint.lat + diffLat, lastPoint.lng + diffLng);
                  }

                  bound.extend(controlPoint);
                  bound.extend(endPoint);

                  endPoint.controlPoint = controlPoint;
                  lastPoint = endPoint;
              } else {
                  bound.extend(coord);
                  lastPoint = new L.latLng(coord[0], coord[1]);
              }
          }
          return bound;
      },

      getCenter: function () {
          return this._bounds.getCenter();
      },

      // _update() is invoked by Path._reset()
      _update: function () {
          if (!this._map) { return; }

          // TODO: consider implementing this._clipPoints(); and this._simplifyPoints(); to improve performance
          this._updatePath();
      },

      _updatePath: function () {
          // the following can be thought of as this._renderer.updateCurve() in both SVG/Canvas renderers
          // similar to Canvas._updatePoly(), Canvas._updateCircle(), etc...
          if (this._usingCanvas) {
              this._updateCurveCanvas();
          } else {
              this._updateCurveSvg();
          }
      },

      //_project() is invoked by Path._reset()
      _project: function () {
          var coord, lastCoord, curCommand, curPoint;

          this._points = [];

          for (var i = 0; i < this._coords.length; i++) {
              coord = this._coords[i];
              if (typeof coord == 'string' || coord instanceof String) {
                  this._points.push(coord);
                  curCommand = coord;
              } else {
                  switch (coord.length) {
                      case 2:
                          curPoint = this._map.latLngToLayerPoint(coord);
                          lastCoord = coord;
                          break;
                      case 1:
                          if (curCommand == 'H') {
                              curPoint = this._map.latLngToLayerPoint([lastCoord[0], coord[0]]);
                              lastCoord = [lastCoord[0], coord[0]];
                          } else {
                              curPoint = this._map.latLngToLayerPoint([coord[0], lastCoord[1]]);
                              lastCoord = [coord[0], lastCoord[1]];
                          }
                          break;
                  }
                  this._points.push(curPoint);
              }
          }

          if (this._bounds.isValid()) {
              var northWestLayerPoint = this._map.latLngToLayerPoint(this._bounds.getNorthWest());
              var southEastLayerPoint = this._map.latLngToLayerPoint(this._bounds.getSouthEast());
              this._rawPxBounds = new L.Bounds(northWestLayerPoint, southEastLayerPoint);
              this._updateBounds();
          }
      },

      _curvePointsToPath: function (points) {
          var point, curCommand, str = '';
          for (var i = 0; i < points.length; i++) {
              point = points[i];
              if (typeof point == 'string' || point instanceof String) {
                  curCommand = point;
                  str += curCommand;
              } else {
                  switch (curCommand) {
                      case 'H':
                          str += point.x + ' ';
                          break;
                      case 'V':
                          str += point.y + ' ';
                          break;
                      default:
                          str += point.x + ',' + point.y + ' ';
                          break;
                  }
              }
          }
          return str || 'M0 0';
      },

      beforeAdd: function (map) {
          L.Path.prototype.beforeAdd.call(this, map);

          this._usingCanvas = this._renderer instanceof L.Canvas;

          if (this._usingCanvas) {
              this._pathSvgElement = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          }
      },

      onAdd: function (map) {
          if (this._usingCanvas) {
              // determine if dash array is set by user
              this._canvasSetDashArray = !this.options.dashArray;
          }

          L.Path.prototype.onAdd.call(this, map); // calls _update()

          if (this._usingCanvas) {
              if (this.options.animate && typeof (TWEEN) === 'object') {
                  this._normalizeCanvasAnimationOptions();

                  this._tweenedObject = { offset: this._pathSvgElement.getTotalLength() };
                  this._tween = new TWEEN.Tween(this._tweenedObject)
                      .to({ offset: 0 }, this.options.animate.duration)
                      // difference of behavior with SVG, delay occurs on every iteration
                      .delay(this.options.animate.delay)
                      .repeat(this.options.animate.iterations - 1)
                      .onComplete(function (scope) {
                          return function () {
                              scope._canvasAnimating = false;
                          }
                      }(this))
                      .start();

                  this._canvasAnimating = true;
                  this._animateCanvas();
              } else {
                  this._canvasAnimating = false;
              }
          } else {
              if (this.options.animate && this._path.animate) {
                  var length = this._svgSetDashArray();

                  this._path.animate([
                      { strokeDashoffset: length },
                      { strokeDashoffset: 0 }
                  ], this.options.animate);
              }
          }
      },

      // SVG specific logic
      _updateCurveSvg: function () {
          this._renderer._setPath(this, this._curvePointsToPath(this._points));

          if (this.options.animate) {
              this._svgSetDashArray();
          }
      },

      _svgSetDashArray: function () {
          var path = this._path;
          var length = path.getTotalLength();

          if (!this.options.dashArray) {
              path.style.strokeDasharray = length + ' ' + length;
          }
          return length;
      },

      // Needed by the `Canvas` renderer for interactivity
      _containsPoint: function (layerPoint) {
          if (!this._bounds.isValid()) {
              return false;
          }
          return this._bounds.contains(this._map.layerPointToLatLng(layerPoint));
      },

      // Canvas specific logic below here
      _normalizeCanvasAnimationOptions: function () {
          var opts = {
              delay: 0,
              duration: 0,
              iterations: 1
          };
          if (typeof (this.options.animate) == "number") {
              opts.duration = this.options.animate;
          } else {
              if (this.options.animate.duration) {
                  opts.duration = this.options.animate.duration;
              }
              if (this.options.animate.delay) {
                  opts.delay = this.options.animate.delay;
              }
              if (this.options.animate.iterations) {
                  opts.iterations = this.options.animate.iterations;
              }
          }

          this.options.animate = opts;
      },

      _updateCurveCanvas: function () {
          var pathString = this._curvePointsToPath(this._points);
          this._pathSvgElement.setAttribute('d', pathString);

          if (this.options.animate && typeof (TWEEN) === 'object' && this._canvasSetDashArray) {
              this.options.dashArray = this._pathSvgElement.getTotalLength() + '';
              this._renderer._updateDashArray(this);
          }

          this._curveFillStroke(new Path2D(pathString), this._renderer._ctx);
      },

      _animateCanvas: function () {
          TWEEN.update();

          // clear out area and re-render all layers
          this._renderer._updatePaths();

          if (this._canvasAnimating) {
              this._animationFrameId = L.Util.requestAnimFrame(this._animateCanvas, this);
          }
      },

      // similar to Canvas._fillStroke(ctx, layer)
      _curveFillStroke: function (path2d, ctx) {
          ctx.lineDashOffset = this._canvasAnimating ? this._tweenedObject.offset : 0.0;

          var options = this.options;

          if (options.fill) {
              ctx.globalAlpha = options.fillOpacity;
              ctx.fillStyle = options.fillColor || options.color;
              ctx.fill(path2d, options.fillRule || 'evenodd');
          }

          if (options.stroke && options.weight !== 0) {
              if (ctx.setLineDash) {
                  ctx.setLineDash(this.options && this.options._dashArray || []);
              }
              ctx.globalAlpha = options.opacity;
              ctx.lineWidth = options.weight;
              ctx.strokeStyle = options.color;
              ctx.lineCap = options.lineCap;
              ctx.lineJoin = options.lineJoin;
              ctx.stroke(path2d);
          }
      },

      // path tracing logic below here
      trace: function (t) {
          // initially map is undefined, but then null if curve was added and removed
          if (this._map === undefined || this._map === null) {
              return [];
          }

          t = t.filter(function (element) {
              return element >= 0 && element <= 1;
          });

          var point, curCommand, curStartPoint, curEndPoint;
          var p1, p2, p3;
          var samples = [];
          for (var i = 0; i < this._points.length; i++) {
              point = this._points[i];
              if (typeof point == 'string' || point instanceof String) {
                  curCommand = point;

                  if (curCommand == 'Z') {
                      samples = samples.concat(this._linearTrace(t, curEndPoint, curStartPoint));
                  }
              } else {
                  switch (curCommand) {
                      case 'M':
                          curStartPoint = point;
                          curEndPoint = point;
                          break;
                      case 'L':
                      case 'H':
                      case 'V':
                          samples = samples.concat(this._linearTrace(t, curEndPoint, point));

                          curEndPoint = point;
                          break;
                      case 'C':
                          p1 = point;
                          p2 = this._points[++i];
                          p3 = this._points[++i];
                          samples = samples.concat(this._cubicTrace(t, curEndPoint, p1, p2, p3));

                          curEndPoint = p3;
                          break;
                      case 'S':
                          p1 = this._reflectPoint(p2, curEndPoint);
                          p2 = point;
                          p3 = this._points[++i];
                          samples = samples.concat(this._cubicTrace(t, curEndPoint, p1, p2, p3));

                          curEndPoint = p3;
                          break;
                      case 'Q':
                          p1 = point;
                          p2 = this._points[++i];
                          samples = samples.concat(this._quadraticTrace(t, curEndPoint, p1, p2));

                          curEndPoint = p2;
                          break;
                      case 'T':
                          p1 = this._reflectPoint(p1, curEndPoint);
                          p2 = point;
                          samples = samples.concat(this._quadraticTrace(t, curEndPoint, p1, p2));

                          curEndPoint = p2;
                          break;
                      default:
                          break;
                  }
              }
          }
          return samples;
      },
      _linearTrace: function (t, p0, p1) {
          return t.map(interval => {
              var x = this._singleLinearTrace(interval, p0.x, p1.x);
              var y = this._singleLinearTrace(interval, p0.y, p1.y);
              return this._map.layerPointToLatLng([x, y]);
          });
      },
      _quadraticTrace: function (t, p0, p1, p2) {
          return t.map(interval => {
              var x = this._singleQuadraticTrace(interval, p0.x, p1.x, p2.x);
              var y = this._singleQuadraticTrace(interval, p0.y, p1.y, p2.y);
              return this._map.layerPointToLatLng([x, y]);
          });
      },
      _cubicTrace: function (t, p0, p1, p2, p3) {
          return t.map(interval => {
              var x = this._singleCubicTrace(interval, p0.x, p1.x, p2.x, p3.x);
              var y = this._singleCubicTrace(interval, p0.y, p1.y, p2.y, p3.y);
              return this._map.layerPointToLatLng([x, y]);
          });
      },
      _singleLinearTrace: function (t, p0, p1) {
          return p0 + t * (p1 - p0);
      },
      _singleQuadraticTrace: function (t, p0, p1, p2) {
          var oneMinusT = 1 - t;
          return Math.pow(oneMinusT, 2) * p0 +
              2 * oneMinusT * t * p1 +
              Math.pow(t, 2) * p2;
      },
      _singleCubicTrace: function (t, p0, p1, p2, p3) {
          var oneMinusT = 1 - t;
          return Math.pow(oneMinusT, 3) * p0 +
              3 * Math.pow(oneMinusT, 2) * t * p1 +
              3 * oneMinusT * Math.pow(t, 2) * p2 +
              Math.pow(t, 3) * p3;
      },
      _reflectPoint: function (point, over) {
          x = over.x + (over.x - point.x);
          y = over.y + (over.y - point.y);
          return L.point(x, y);
      }
  });

  L.curve = function (path, options) {
      return new L.Curve(path, options);
  };
}

//
// DEFAULT MAP SETTINGS
//

const attribution = ref('&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors')
const url = ref('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
const mapOptions = ref({ zoomSnap: 0.2, zoomControl: false, maxZoom: 40 })
const forcingUpdateMap = ref(false)

export const useMapHelpers = () => {
  return {
    attribution: computed(() => attribution.value),
    url: computed(() => url.value),
    mapOptions: computed(() => mapOptions.value),
    forcingUpdateMap,
    forceUpdateMap: async () => {
      forcingUpdateMap.value = true
      await nextTick()
      forcingUpdateMap.value = false
    }
  }
}

//
// BOUNDS
//

const curveHasBeenDefined = ref(false)
const mapsBoundGroups = ref({ empty: [] })
const mapsPadding = ref({})
const defaultCoords = ref([{ lat: "-25.255892", lng: "-57.725735" }, { lat: "-25.368553", lng: "-57.456055" }])

export const useMapBounds = map => {

  const mapId = computed(() => map.value?._leaflet_id || -1)

  const padding = computed(() => /*mapsPadding.value[mapId.value] || */[5, 1, 15, 1])
  const listToBound = computed(() => {
    const result = Object.values(mapsBoundGroups.value[mapId.value]).reduce((result, group) => [...result, ...(group || [])], [])
    return result.length === 0 ? defaultCoords.value : result
  })

  const bounds = computed(() => {
    let firstSelected = false
    let maxLat = 0.0,
      maxLng = 0.0,
      minLat = 0.0,
      minLng = 0.0
    for (let elem of listToBound.value) {
      if (!elem || !(elem.lat || elem[1]) || !(elem.lng || elem[0]) || elem.lat === 'null' || elem.lng === 'null') continue
      const lat = parseFloat(elem.lat || elem[1])
      const lng = parseFloat(elem.lng || elem[0])
      if (lat > maxLat || !firstSelected) maxLat = lat
      if (lat < minLat || !firstSelected) minLat = lat
      if (lng > maxLng || !firstSelected) maxLng = lng
      if (lng < minLng || !firstSelected) minLng = lng
      firstSelected = true
    }
    const mult = 0.02 * 0.25
    const [p1, p2, p3, p4] = Array.isArray(padding.value) ?
      [padding.value[0] * mult, padding.value[1] * mult, padding.value[2] * mult, padding.value[3] * mult] :
      [padding.value * mult, padding.value * mult, padding.value * mult, padding.value * mult]

    return [
      [maxLat + p1, maxLng + p2],
      [minLat - p3, minLng - p4]
    ]
  })

  const setMapBoundGroup = (groupName, groupValue) => {
    if (!mapsBoundGroups.value[mapId.value]) mapsBoundGroups.value[mapId.value] = {}
    mapsBoundGroups.value[mapId.value][groupName] = groupValue
    mapsBoundGroups.value = { ...mapsBoundGroups.value }
  }
  const setMapPadding = padding => {
    if (!mapsPadding.value[mapId.value]) mapsPadding.value[mapId.value] = []
    mapsPadding.value[mapId.value] = padding
    mapsPadding.value = { ...mapsPadding.value }
  }

  return {
    setMapPadding,
    setMapBoundGroup,
    updateBounds: () => map.value.fitBounds(bounds.value),
  }
}

export const useMapDistance = () => {
  const distanceToCurrentPosition = coords => {
    const { currentPosition, positionError } = useLocation()
    if (positionError.value ||
      !currentPosition.value ||
      !currentPosition.value.lat ||
      !currentPosition.value.lng ||
      !coords ||
      !coords.lat ||
      !coords.lng) return null

    return distanceBetween(
      currentPosition.value.lat,
      currentPosition.value.lng,
      coords.lat,
      coords.lng
    )
  }

  return {
    distanceToCurrentPosition,
  }
}

export const useMapCurve = (map, points) => {
  if (!curveHasBeenDefined.value) {
    defineCurve()
    curveHasBeenDefined.value = true
  }

  const curve = ref(null)

  const curvePoints = () => {
    if (points.value.length !== 2 ||
        !points.value[0] ||
        !points.value[1] ||
        !points.value[0].lat ||
        !points.value[1].lat) return []

    const latlng1 = [points.value[0].lat, points.value[0].lng]
    const latlng2 = [points.value[1].lat, points.value[1].lng]

    const offsetX = latlng2[1] - latlng1[1]
    const offsetY = latlng2[0] - latlng1[0]

    const r = Math.sqrt(Math.pow(offsetX, 2) + Math.pow(offsetY, 2))
    const theta = Math.atan2(offsetY, offsetX)

    const thetaOffset = (3.14 / 10)

    const r2 = (r / 2) / (Math.cos(thetaOffset))
    const theta2 = theta + thetaOffset

    const midpointX = (r2 * Math.cos(theta2)) + parseFloat(latlng1[1])
    const midpointY = (r2 * Math.sin(theta2)) + parseFloat(latlng1[0])

    return [latlng1, [midpointY, midpointX], latlng2]
  }

  const drawCurve = () => {
    const [latlng1, midpointLatLng, latlng2] = curvePoints()
    if (!latlng1 || !midpointLatLng || !latlng2) {
      if (curve.value) {
        curve.value.setPath([])
        curve.value = null
      }
      return
    }
    const pathOptions = {color: '#223377', weight: 5}
    const path = ['M', latlng1, 'Q', midpointLatLng, latlng2]
    if (!curve.value) curve.value = L.curve(path, pathOptions).addTo(map.value);
    else curve.value.setPath(path)
    return curve.value
  }

  return {
    drawCurve
  }
}

