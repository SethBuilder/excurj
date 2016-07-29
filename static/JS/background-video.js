/**
 * Full Background Video
 *
 * More info on Audio/Video Media Events/Attributes/Methods
 * - https://developer.mozilla.org/en-US/docs/Web/Guide/Events/Media_events
 * - http://www.w3schools.com/tags/ref_av_dom.asp
 */

(function (global) {

  // Define BackgroundVideo constructor on the global object
  global.BackgroundVideo = function () {

    // Plugin options
    this.opt = null;
    // The Video element
    this.videoEl = null;

    // Approximate Loading Rate
    //
    // The value will be a number like 0.8
    // which means to load 4 seconds of the video
    // it takes 5 seconds. If the number is super low
    // like 0.2 (regular 3g connections) then you can
    // decide whether to play the video or not.
    // This behaviour will be controller with
    // the `acceptableLoadingRate` option.
    this.approxLoadingRate = null;

    // Methods to which `this` will be bound
    this._resize = null;
    this._progress = null;

    // Time at which video is initialized
    this.startTime = null;

    // Initialize and setup the video in DOM`
    this.init = function (opt) {
      // If not set then set to an empty object
      this.opt = opt = opt || {};

      var self = this;

      self._resize = self.resize.bind(this);
      self._progress = self.progress.bind(this);

      // Video element
      self.videoEl = opt.videoEl;

      // Meta data event
      self.videoEl.addEventListener('loadedmetadata', self._resize, false);
      // Progress event for buffer data
      self.videoEl.addEventListener('progress', self._progress, false);

      // Fired when enough has been buffered to begin the video
      // self.videoEl.readyState === 4 (HAVE_ENOUGH_DATA)
      self.videoEl.addEventListener('canplay', function () {
        self.opt.onLoad && self.opt.onLoad();
      });

      // window.videoEl = this.videoEl;

      // If resizing is required (resize video as window/container resizes)
      if (self.opt.resize) {
        global.addEventListener('resize', self._resize, false);
      }

      // Start time of video initialization
      this.startTime = (new Date()).getTime();

      // Create `source` for video
      this.opt.src.forEach(function (srcOb, i, arr) {
        var key
          , val
          , source = document.createElement('source');

        // Set all the attribute key=val supplied in `src` option
        for (key in srcOb) {
          if (srcOb.hasOwnProperty(key)) {
            val = srcOb[key];

            source.setAttribute(key, val);
          }
        }

        self.videoEl.appendChild(source);
      });

      return;
    }

    // Called once video metadata is available
    //
    // Also called when window/container is resized
    this.resize = function () {
      // Video's intrinsic dimensions
      var w = this.videoEl.videoWidth
        , h = this.videoEl.videoHeight;

      // Intrinsic ratio
      // Will be more than 1 if W > H and less if W < H
      var videoRatio = (w / h).toFixed(2);

      // Get the container DOM element and its styles
      //
      // Also calculate the min dimensions required (this will be
      // the container dimentions)
      var container = this.opt.container
        , containerStyles = global.getComputedStyle(container)
        , minW = parseInt( containerStyles.getPropertyValue('width') )
        , minH = parseInt( containerStyles.getPropertyValue('height') );

      // If !border-box then add paddings to width and height
      if (containerStyles.getPropertyValue('box-sizing') !== 'border-box') {
        var paddingTop = containerStyles.getPropertyValue('padding-top')
          , paddingBottom = containerStyles.getPropertyValue('padding-bottom')
          , paddingLeft = containerStyles.getPropertyValue('padding-left')
          , paddingRight = containerStyles.getPropertyValue('padding-right');

        paddingTop = parseInt(paddingTop);
        paddingBottom = parseInt(paddingBottom);
        paddingLeft = parseInt(paddingLeft);
        paddingRight = parseInt(paddingRight);

        minW += paddingLeft + paddingRight;
        minH += paddingTop + paddingBottom;
      }

      // What's the min:intrinsic dimensions
      //
      // The idea is to get which of the container dimension
      // has a higher value when compared with the equivalents
      // of the video. Imagine a 1200x700 container and
      // 1000x500 video. Then in order to find the right balance
      // and do minimum scaling, we have to find the dimension
      // with higher ratio.
      //
      // Ex: 1200/1000 = 1.2 and 700/500 = 1.4 - So it is best to
      // scale 500 to 700 and then calculate what should be the
      // right width. If we scale 1000 to 1200 then the height
      // will become 600 proportionately.
      var widthRatio = minW / w;
      var heightRatio = minH / h;

      // Whichever ratio is more, the scaling
      // has to be done over that dimension
      if (widthRatio > heightRatio) {
        var newWidth = minW;
        var newHeight = Math.ceil( newWidth / videoRatio );
      }
      else {
        var newHeight = minH;
        var newWidth = Math.ceil( newHeight * videoRatio );
      }

      this.videoEl.style.width = newWidth + 'px';
      this.videoEl.style.height = newHeight + 'px';
    };

    this.progress = function (e) {
      // Duration of the video (in seconds)
      var duration = this.videoEl.duration
        , currentTime = this.videoEl.currentTime
        , buffer = this.videoEl.buffered;

      // Not sure why this happens at times
      if (buffer.length === 0) return;
      if (!this.opt.minBuffer) this.videoEl.play();

      // Buffered seconds
      var bufferedLength = buffer.length;
      var bufferedSeconds = (
        buffer.end(bufferedLength - 1)
        -
        buffer.start(bufferedLength - 1)
      );

      // console.log(bufferedSeconds - currentTime)

      // Close to the end
      if (duration - currentTime < this.opt.minBuffer) {
        // If the video is not playing
        if (this.videoEl.paused) {
          this.videoEl.play();
        }
      }
      else {
        if (bufferedSeconds - currentTime > this.opt.minBuffer) {
          // Video is starting for the first time
          if (currentTime === 0 && this.opt.acceptableLoadingRate) {
            var endTime = (new Date()).getTime();

            var diffDuration = (endTime - this.startTime) / 1000;
            var approxLoadingRate = this.opt.minBuffer / diffDuration;

            if (this.opt.acceptableLoadingRate.value) {
              if (approxLoadingRate >= this.opt.acceptableLoadingRate.value) {
                this.videoEl.play();
              }
              else {
                if (this.opt.acceptableLoadingRate.stopBuffering) {
                  this.videoEl.src = '';
                }

                if (this.opt.acceptableLoadingRate.callback) {
                  this.opt.acceptableLoadingRate.callback();
                }
              }
            }
            else {
              this.videoEl.play();
            }
          }
          else {
            this.videoEl.play();
          }
        }
        else if (bufferedSeconds - currentTime <= 1) {
          this.videoEl.pause();
        }
      }
    }

  };

}(window));
