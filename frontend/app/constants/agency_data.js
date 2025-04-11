export const AGENCY_DATA = [
    {
      agency_id: "1",
      agency_name: 'SCTP Iasi',
      city: 'Iasi',
      agency_url: 'https://www.sctpiasi.ro/',
      agency_timezone: 'Europe/Bucharest',
      agency_lang: 'ro',
    },
    {
      agency_id: "2",
      agency_name: 'CTP Cluj',
      city: 'Cluj-Napoca',
      agency_url: 'https://www.ctpcluj.ro/',
      agency_timezone: 'Europe/Bucharest',
      agency_lang: 'ro',
    },
    {
      agency_id: "4",
      agency_name: 'RTEC&PUA Chisinau',
      city: 'Chisinau',
      agency_url: 'https://www.rtec.md/',
      agency_timezone: 'Europe/Bucharest',
      agency_lang: 'ro',
    },
    {
      agency_id: "6",
      agency_name: 'Eltrans Botosani',
      city: 'Botosani',
      agency_url: 'https://www.eltransbt.ro/',
      agency_timezone: 'Europe/Bucharest',
      agency_lang: 'ro',
    },
    {
      agency_id: "8",
      agency_name: 'STPT Timisoara',
      city: 'Timisoara',
      agency_url: 'https://www.ratt.ro/',
      agency_timezone: 'Europe/Bucharest',
      agency_lang: 'ro',
    },
    {
      agency_id: "9",
      agency_name: 'OTL Oradea',
      city: 'Oradea',
      agency_url: 'https://www.otlra.ro/',
      agency_timezone: 'Europe/Bucharest',
      agency_lang: 'ro',
    }
  ];
  
  export const getCityByAgencyId = (agencyId) => {
    const agency = AGENCY_DATA.find(a => a.agency_id === agencyId);
    return agency ? agency.city : null;
  };
  
  export const getAgencyIdByCity = (city) => {
    const agency = AGENCY_DATA.find(a => a.city.toLowerCase() === city.toLowerCase());
    return agency ? agency.agency_id : null;
  };
  
  export const getAllCities = () => {
    return AGENCY_DATA.map(agency => agency.city);
  };