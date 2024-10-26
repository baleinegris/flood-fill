#!/bin/sh

thispath="$(dirname "$(realpath "$0")")"
cd "$thispath" || exit 1

get_precip_data(){
	time=$1
	scenario=$2
	if [ "$time" == "historical" ]; then
		file="1950-2014_ECCC_CanDCSU6_Precip-Pct50_Sfc_LatLon0.86_P1Y.nc"
		url="https://dd.weather.gc.ca/climate/candcsu6/10km/historical/${file}"
	elif [ "$time" == "scenario" ]; then
		scenario_cap="$(echo $scenario | tr a-z A-Z)"
		file="2015-2100_ECCC_CanDCSU6-${scenario_cap}_Precip-Pct50_Sfc_LatLon0.86_P1Y.nc"
		url="https://dd.weather.gc.ca/climate/candcsu6/10km/scenarios/${scenario}/${file}"
	fi
	
	if [ -f "$file" ]; then
		printf '##### %s already exists #####\n' "$file"
	else
		printf '##### GET %s %s: %s #####\n' "$time" "$scenario" "$file"
		wget "$url" || exit 1
	fi
}

get_precip_data historical
for scenario in ssp126 ssp245 ssp585; do
	get_precip_data scenario "$scenario"
done
