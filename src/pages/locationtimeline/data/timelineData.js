export const coaches = [
  { id: 0, content: "Murad Hesham" },
  { id: 1, content: "Brian Kasumba" },
  { id: 2, content: "Majille Malijan" },
  { id: 3, content: "Clinton Oduro" },
  { id: 4, content: "Jelili Alimi" },
  { id: 5, content: "Dave Clinton Salas" },
  { id: 6, content: "Godfrey Odong" },
  { id: 7, content: "Amir Parvizi" },
  { id: 8, content: "Godfrey Odong" },
  { id: 9, content: "Abdoulaye Diallo" },
  { id: 10, content: "Lamine Ndiaye" },
  { id: 11, content: "Majille Malijon" }
];

export const locations = [
    { 'id': 1, 'content': 'Amity School', 'nestedGroups': [10, 11, 21] },
    { 'id': 2, 'content': 'Amity School Abu Dhabi', 'nestedGroups': [12, 13] },
    { 'id': 3, 'content': 'Al Nasr Club', 'nestedGroups': [14] },
    { 'id': 4, 'content': 'Al Wasl Club', 'nestedGroups': [15, 16, 17] },
    { 'id': 5, 'content': 'Brighton College', 'nestedGroups': [18, 19, 20] },
    { 'id': 6, 'content': 'Dubai International Academy', 'nestedGroups': [22, 23, 24, 25] },
    { 'id': 7, 'content': 'Durham School', 'nestedGroups': [26, 27] },
    { 'id': 8, 'content': 'German International School', 'nestedGroups': [28] },
    { 'id': 9, 'content': 'Jebel Ali School', 'nestedGroups': [29, 30, 31] },
    { 'id': 10, 'content': 'Sports Hall Court 1' },
    { 'id': 11, 'content': 'Sports Hall' },
    { 'id': 12, 'content': 'Primary Sports Hall' },
    { 'id': 13, 'content': 'Secondary Sports Hall' },
    { 'id': 14, 'content': 'Ground fl Sports Hall' },
    { 'id': 15, 'content': 'Primary Sports Hall Court 1' },
    { 'id': 16, 'content': 'Secondary Sports Hall Court 1' },
    { 'id': 17, 'content': 'Secondary Sports Hall Court 2' },
    { 'id': 18, 'content': 'Sports Center Court 1' },
    { 'id': 19, 'content': 'Sports Center Court 2' },
    { 'id': 20, 'content': 'Sports Center Court 3' },
    { 'id': 21, 'content': 'Sports Hall Court 2' },
    { 'id': 22, 'content': 'Court 1' },
    { 'id': 23, 'content': 'Court 2' },
    { 'id': 24, 'content': 'Court 3' },
    { 'id': 25, 'content': 'Court 4' },
    { 'id': 26, 'content': 'Full Court 1' },
    { 'id': 27, 'content': 'Full Court 2' },
    { 'id': 28, 'content': 'Outdoor Track' },
    { 'id': 29, 'content': 'Multipurpose Hall 1' },
    { 'id': 30, 'content': 'Multipurpose Hall 2' },
    { 'id': 31, 'content': 'Multipurpose Hall' }
];

export const items = [
    {
        id: 37,
        group: 10,
        start: '2023-11-14 12:30:00',
        end: '2023-11-14 14:30:00',
        _type: 'office',
        data: { coach: 'Godfrey Odong' }
      },
      {
        id: 36,
        group: 10,
        start: '2023-11-14 15:30:00',
        end: '2023-11-14 16:00:00',
        _type: 'lunch',
        data: { coach: 'Brian Kasumba' }
      },
      {
        id: 0,
        group: 10,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 3,
          age_group: '5 - 7',
          term: 'Term 1a',
          coach: 'Amir Parvizi'
        },
        start: '2023-11-14 16:30:00',
        end: '2023-11-14 17:30:00',
        _type: 'dubai'
      },
      {
        id: 1,
        group: 10,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 2,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Abdoulaye Diallo'
        },
        start: '2023-11-14 17:30:00',
        end: '2023-11-14 18:30:00',
        _type: 'dubai'
      },
      {
        id: 2,
        group: 10,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 7,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Godfrey Odong'
        },
        start: '2023-11-14 18:30:00',
        end: '2023-11-14 19:30:00',
        _type: 'dubai'
      },
      {
        id: 3,
        group: 10,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Int A',
          seats_taken: 4,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Murad Hesham'
        },
        start: '2023-11-14 19:30:00',
        end: '2023-11-14 20:30:00',
        _type: 'dubai'
      },
      {
        id: 43,
        group: 11,
        start: '2023-11-14 10:00:00',
        end: '2023-11-14 11:00:00',
        _type: 'office',
        data: { coach: 'Clinton Oduro' }
      },
      {
        id: 38,
        group: 11,
        start: '2023-11-14 14:00:00',
        end: '2023-11-14 14:30:00',
        _type: 'lunch',
        data: { coach: 'Amir Parvizi' }
      },
      {
        id: 48,
        group: 11,
        start: '2023-11-14 14:30:00',
        end: '2023-11-14 15:00:00',
        _type: 'buffer',
        data: { coach: 'Abdoulaye Diallo' }
      },
      {
        id: 4,
        group: 11,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 12,
          age_group: '5 - 7',
          term: 'Term 1a',
          coach: 'Dave Clinton Salas'
        },
        start: '2023-11-14 15:00:00',
        end: '2023-11-14 16:00:00',
        _type: 'dubai'
      },
      {
        id: 5,
        group: 11,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 9,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Abdoulaye Diallo'
        },
        start: '2023-11-14 16:00:00',
        end: '2023-11-14 17:00:00',
        _type: 'dubai'
      },
      {
        id: 6,
        group: 11,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 4,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Amir Parvizi'
        },
        start: '2023-11-14 17:00:00',
        end: '2023-11-14 18:00:00',
        _type: 'dubai'
      },
      {
        id: 7,
        group: 11,
        data: {
          program: 'ASA',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 2,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Lamine Ndiaye'
        },
        start: '2023-11-14 12:15:00',
        end: '2023-11-14 13:15:00',
        _type: 'dubai'
      },
      {
        id: 44,
        group: 12,
        start: '2023-11-14 10:00:00',
        end: '2023-11-14 11:00:00',
        _type: 'office',
        data: { coach: 'Godfrey Odong' }
      },
      {
        id: 39,
        group: 12,
        start: '2023-11-14 14:00:00',
        end: '2023-11-14 15:00:00',
        _type: 'lunch',
        data: { coach: 'Dave Clinton Salas' }
      },
      {
        id: 8,
        group: 12,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 3,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Abdoulaye Diallo'
        },
        start: '2023-11-14 18:00:00',
        end: '2023-11-14 19:00:00',
        _type: 'sharjah'
      },
      {
        id: 9,
        group: 12,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 6,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Clinton Oduro'
        },
        start: '2023-11-14 19:00:00',
        end: '2023-11-14 20:00:00',
        _type: 'sharjah'
      },
      {
        id: 45,
        group: 13,
        start: '2023-11-14 10:00:00',
        end: '2023-11-14 11:00:00',
        _type: 'office',
        data: { coach: 'Abdoulaye Diallo' }
      },
      {
        id: 40,
        group: 13,
        start: '2023-11-14 14:00:00',
        end: '2023-11-14 15:00:00',
        _type: 'lunch',
        data: { coach: 'Jelili Alimi' }
      },
      {
        id: 10,
        group: 13,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 4,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Jelili Alimi'
        },
        start: '2023-11-14 17:00:00',
        end: '2023-11-14 18:00:00',
        _type: 'sharjah'
      },
      {
        id: 11,
        group: 13,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 3,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Godfrey Odong'
        },
        start: '2023-11-14 18:00:00',
        end: '2023-11-14 19:00:00',
        _type: 'sharjah'
      },
      {
        id: 46,
        group: 14,
        start: '2023-11-14 10:00:00',
        end: '2023-11-14 11:00:00',
        _type: 'office',
        data: { coach: 'Godfrey Odong' }
      },
      {
        id: 41,
        group: 14,
        start: '2023-11-14 14:00:00',
        end: '2023-11-14 15:00:00',
        _type: 'lunch',
        data: { coach: 'Brian Kasumba' }
      },
      {
        id: 12,
        group: 14,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 3,
          age_group: '5 - 7',
          term: 'Term 1a',
          coach: 'Dave Clinton Salas'
        },
        start: '2023-11-14 17:00:00',
        end: '2023-11-14 18:00:00',
        _type: 'sharjah'
      },
      {
        id: 13,
        group: 14,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Int B',
          seats_taken: 10,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Dave Clinton Salas'
        },
        start: '2023-11-14 18:00:00',
        end: '2023-11-14 19:00:00',
        _type: 'sharjah'
      },
      {
        id: 47,
        group: 15,
        start: '2023-11-14 10:00:00',
        end: '2023-11-14 11:00:00',
        _type: 'office',
        data: { coach: 'Abdoulaye Diallo' }
      },
      {
        id: 42,
        group: 15,
        start: '2023-11-14 14:00:00',
        end: '2023-11-14 15:00:00',
        _type: 'lunch',
        data: { coach: 'Murad Hesham' }
      },
      {
        id: 14,
        group: 15,
        data: {
          program: "Balln'Babies",
          class_type: 'Youth Mixed',
          level: 'Tod',
          seats_taken: 0,
          age_group: '2 - 3',
          term: 'Term 1a',
          coach: 'Majille Malijon'
        },
        start: '2023-11-14 12:00:00',
        end: '2023-11-14 13:00:00'
      },
      {
        id: 15,
        group: 15,
        data: {
          program: "Balln'Babies",
          class_type: 'Youth Mixed',
          level: 'Tod',
          seats_taken: 2,
          age_group: '3 - 5',
          term: 'Term 1a',
          coach: 'Jelili Alimi'
        },
        start: '2023-11-14 13:00:00',
        end: '2023-11-14 14:00:00'
      },
      {
        id: 16,
        group: 16,
        data: {
          program: "Balln'Babies",
          class_type: 'Youth Mixed',
          level: 'Tod',
          seats_taken: 5,
          age_group: '3 - 5',
          term: 'Term 1a',
          coach: 'Murad Hesham'
        },
        start: '2023-11-14 14:00:00',
        end: '2023-11-14 15:00:00'
      },
      {
        id: 17,
        group: 16,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Int A',
          seats_taken: 2,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Godfrey Odong'
        },
        start: '2023-11-14 15:00:00',
        end: '2023-11-14 16:00:00'
      },
      {
        id: 18,
        group: 16,
        data: {
          program: "Balln'Babies",
          class_type: 'Youth Mixed',
          level: 'Tod',
          seats_taken: 5,
          age_group: '3 - 5',
          term: 'Term 1a',
          coach: 'Lamine Ndiaye'
        },
        start: '2023-11-14 16:00:00',
        end: '2023-11-14 17:00:00'
      },
      {
        id: 19,
        group: 16,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 5,
          age_group: '5 - 7',
          term: 'Term 1a',
          coach: 'Brian Kasumba'
        },
        start: '2023-11-14 17:00:00',
        end: '2023-11-14 18:00:00'
      },
      {
        id: 20,
        group: 17,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Int B',
          seats_taken: 5,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Murad Hesham'
        },
        start: '2023-11-14 15:00:00',
        end: '2023-11-14 16:00:00'
      },
      {
        id: 21,
        group: 17,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 11,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Amir Parvizi'
        },
        start: '2023-11-14 16:00:00',
        end: '2023-11-14 17:00:00'
      },
      {
        id: 22,
        group: 17,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 12,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Majille Malijon'
        },
        start: '2023-11-14 17:00:00',
        end: '2023-11-14 18:00:00'
      },
      {
        id: 23,
        group: 18,
        data: {
          program: 'Adult Academy',
          class_type: 'Adult Mixed',
          level: 'Adult',
          seats_taken: 8,
          age_group: '18+',
          term: 'Term 1a',
          coach: 'Dave Clinton Salas'
        },
        start: '2023-11-14 19:00:00',
        end: '2023-11-14 20:00:00'
      },
      {
        id: 24,
        group: 19,
        data: {
          program: 'Youth Academy',
          class_type: 'All Boys',
          level: 'Int B',
          seats_taken: 2,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Jelili Alimi'
        },
        start: '2023-11-14 11:00:00',
        end: '2023-11-14 12:00:00'
      },
      {
        id: 25,
        group: 19,
        data: {
          program: 'Youth Academy',
          class_type: 'All Girls',
          level: 'Beg',
          seats_taken: 8,
          age_group: '10 - 18',
          term: 'Term 1a',
          coach: 'Jelili Alimi'
        },
        start: '2023-11-14 15:00:00',
        end: '2023-11-14 16:00:00'
      },
      {
        id: 26,
        group: 19,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 2,
          age_group: '5 - 7',
          term: 'Term 1a',
          coach: 'Majille Malijan'
        },
        start: '2023-11-14 16:00:00',
        end: '2023-11-14 17:00:00'
      },
      {
        id: 27,
        group: 19,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 15,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Majille Malijan'
        },
        start: '2023-11-14 17:00:00',
        end: '2023-11-14 18:00:00'
      },
      {
        id: 28,
        group: 19,
        data: {
          program: 'Youth Academy',
          class_type: 'All Boys',
          level: 'Beg',
          seats_taken: 8,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Dave Clinton Salas'
        },
        start: '2023-11-14 18:00:00',
        end: '2023-11-14 19:00:00'
      },
      {
        id: 29,
        group: 19,
        data: {
          program: 'Youth Academy',
          class_type: 'All Boys',
          level: 'Int B',
          seats_taken: 6,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Dave Clinton Salas'
        },
        start: '2023-11-14 19:00:00',
        end: '2023-11-14 20:00:00'
      },
      {
        id: 30,
        group: 15,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 5,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Brian Kasumba'
        },
        start: '2023-11-14 16:00:00',
        end: '2023-11-14 17:00:00'
      },
      {
        id: 31,
        group: 15,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Int A',
          seats_taken: 0,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Amir Parvizi'
        },
        start: '2023-11-14 17:00:00',
        end: '2023-11-14 18:00:00'
      },
      {
        id: 32,
        group: 20,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 3,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Majille Malijon'
        },
        start: '2023-11-14 15:00:00',
        end: '2023-11-14 16:00:00',
        _type: 'abudhabi'
      },
      {
        id: 33,
        group: 20,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 3,
          age_group: '12 - 18',
          term: 'Term 1a',
          coach: 'Jelili Alimi'
        },
        start: '2023-11-14 16:00:00',
        end: '2023-11-14 17:00:00',
        _type: 'abudhabi'
      },
      {
        id: 34,
        group: 21,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 4,
          age_group: '5 - 7',
          term: 'Term 1a',
          coach: 'Godfrey Odong'
        },
        start: '2023-11-14 15:00:00',
        end: '2023-11-14 16:00:00',
        _type: 'abudhabi'
      },
      {
        id: 35,
        group: 12,
        data: {
          program: 'Youth Academy',
          class_type: 'Youth Mixed',
          level: 'Beg',
          seats_taken: 8,
          age_group: '8 - 11',
          term: 'Term 1a',
          coach: 'Lamine Ndiaye'
        },
        start: '2023-11-14 16:00:00',
        end: '2023-11-14 17:00:00',
        _type: 'abudhabi'
    }
];
