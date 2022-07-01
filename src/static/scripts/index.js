Vue.component('area-select', {
    template: '#area-selector-template',
    props: ["countries", "countryLoading"],
    data() {
        return {
            states: [],
            admin2s: [],
            selectedCountry: "",
            selectedState: "",
            selectedAdmin2: "",
            countriesLoading: false,
            statesLoading: false,
            admin2sLoading: false,
            countriesDisabled: false,
            statesDisabled: true,
            admin2sDisabled: true,

            countrySearch:""
        }
    },
})

var vueApp = new Vue({
    el: "#app",
    vuetify: new Vuetify(),
    data: {
        drawer: false,
        tab: "",

        countries: [],

        tableHeaders: [
            { text: 'Country/region', value: '0' },
            { text: 'Confirmed', value: '1' },
            { text: 'Deaths', value: '2' },
            { text: 'Recovered', value: '3' },
        ],
        tableData: [],
        tableLoading: false,

        historyTableHeaders: [
            { text: "Date", value: "0" },
            { text: 'Confirmed', value: '1' },
            { text: 'Deaths', value: '2' },
            { text: 'Recovered', value: '3' },
        ],
        historyTableData: [],
        historyTableLoading: false,

        chartOptions: {
            chart: {
                zoomType: "x",
                height:800
            },
            title: {
                text: "Unset"
            },
            series: [
                {
                    name: "Confirmed",
                    data: []
                },
                {
                    name: "Deaths",
                    data: []
                },
                {
                    name: "New confirmed",
                    data: {}
                },
                {
                    name: "New deaths",
                    data: {}
                }
            ],
            xAxis: {
                type: 'datetime',
                /* labels: {
                  formatter: function () {
                    return Highcharts.dateFormat('%e %b', this.value * 1000); // milliseconds not seconds
                  },
                } */
            }
        },

    },
    created: function () {
        this.loadCountries();
        this.loadCountriesDataTable();
        this.loadWorldHistoryDataTable();
    },
    methods: {
        loadCountries: function () {
            this.countriesLoading = true;
            fetch('api/list/country')
                .then((response) => {
                    this.countriesLoading = false;
                    return response.json();
                })
                .then((data) => {
                    this.countries = data;
                });
        },
        loadCountriesDataTable: function () {
            this.tableLoading = true;
            fetch('/api/table/data/country')
                .then((response) => {
                    this.tableLoading = false;
                    return response.json();
                })
                .then((data) => {
                    this.tableData = data;
                });
        },
        loadWorldHistoryDataTable: function () {
            this.historyTableLoading = true;
            fetch('/api/table/history/world')
                .then((response) => {
                    this.historyTableLoading = false;
                    return response.json();
                })
                .then((data) => {
                    this.chartOptions.title.text = "History"
                    this.historyTableData = data;
                    this.populateChart(data)
                });
        },
        populateChart: function (data) {
            data0 = [];
            data1 = [];
            data2 = [];
            data3 = [];
            prevConfirmed = 0;
            prevDeath = 0;
            data.forEach(item => {
                data0.push([new Date(item[0]).getTime(), item[1]]);
                data1.push([new Date(item[0]).getTime(), item[2]]);
                data2.push([new Date(item[0]).getTime(), item[1] - prevConfirmed]);
                data3.push([new Date(item[0]).getTime(), item[2] - prevDeath]);
                prevConfirmed = item[1];
                prevDeath = item[2];
            })
            this.chartOptions.series[0].data = data0;
            this.chartOptions.series[1].data = data1;
            this.chartOptions.series[2].data = data2;
            this.chartOptions.series[3].data = data3;
        },

    }
})