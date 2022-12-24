window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, x_cory_cor, context) {
            const {
                min,
                max,
                circleOptions,
                colorProp
            } = context.props.hideout;
            //console.log('feature', feature);
            let colors = ["brown", "blue", "green", "yellow", "orange", "red"];
            circleOptions.fillColor = colors[feature.properties['road_type']]; // set color based on color prop.
            return L.circleMarker(x_cory_cor, circleOptions); // sender a simple circle marker.
        },
        function1: function(feature, x_cory_cor, index, context) {
            const {
                min,
                max,
                circleOptions,
                colorProp,
                count,
                colors
            } = context.props.hideout;

            const leaves = index.getLeaves(feature.properties.cluster_id, feature.properties.point_count);
            //let colors = ["brown", "blue", "green", "yellow", "orange", "red"];
            let valueSum = new Array(count).fill(0)
            //let valueSum = [0,0,0,0,0,0];
            for (let i = 0; i < leaves.length; ++i) {
                valueSum[leaves[i].properties[colorProp]] += 1
            }

            for (let i = 0; i < valueSum.length; ++i) {
                valueSum[i] /= leaves.length;
                valueSum[i] *= 100;
            }

            let cumSum = 0
            let gradient = 'background: conic-gradient(';
            //console.log('val ', valueSum);
            for (let i = 0; i < valueSum.length; ++i) {
                if (valueSum[i] != 0) {
                    if (cumSum == 0) {
                        if (valueSum[i] == 100) {
                            gradient += 'red 0.01%, ' + colors[i] + ' 0.01%';
                            break;
                        }
                        cumSum += valueSum[i];
                        gradient += colors[i] + ' ' + cumSum.toString() + '%, ';
                        continue;
                    }
                    gradient += colors[i] + ' ' + cumSum.toString() + '% ';

                    if (100 - (cumSum + valueSum[i]) < 0.000001) {
                        break;
                    }
                    cumSum += valueSum[i];
                    gradient += cumSum.toString() + '%, ';
                }
            }


            //console.log('grad: ', gradient);


            //const valueMean = valueSum / leaves.length;
            // Render a circle with the number of leaves written in the center.

            //console.log(leaves.length, valueSum);
            //console.log(feature);
            //console.log(index);
            //console.log(leaves);

            const icon = L.divIcon.scatter({
                html: '<div style="margin: 0; border-radius: 50%; padding-top: 6px; height: 34px; width: 40px; ' + gradient + ')"><div style="margin: 0; height: 28px; width: 28px; background-color:white; border-radius: 50%; margin-left: auto; margin-right: auto;"><span>' + feature.properties.point_count_abbreviated + '</span></div></div>',
                className: "marker-cluster",
                iconSize: L.point(40, 40),
            });
            return L.marker(x_cory_cor, {
                icon: icon
            });
        }
    }
});