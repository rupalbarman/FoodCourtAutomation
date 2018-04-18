'''
	Lazy implementation of cache lel
'''

users = [
	{
		'username'	 : 'rupal',
		'password'   : 'barman'
	},
	{
		'username'   : 'susan',
		'password'   : 'gabriel'
	}
]

restaurent_items = [
	{
		'id'	:	1,
		'name'	:	'dominos',
		'items' : [
			{
				'name'	:	'pizza',
				'price'	:	12.34,
				'id'	:	'1_01'
			},
			{
				'name'	:	'burger',
				'price'	:	22.34,
				'id'	:	'1_02'
			},
			{
				'name'	:	'calzone',
				'price'	:	29.34,
				'id'	:	'1_03'
			}
		]
	},
	{
		'id'	:	2,
		'name'	:	'pizzahut',
		'items' : [
			{
				'name'	:	'pizza big',
				'price'	:	18.34,
				'id'	:	'2_01'
			},
			{
				'name'	:	'burger small',
				'price'	:	42.34,
				'id'	:	'2_02'
			},
			{
				'name'	:	'french fries',
				'price'	:	49.34,
				'id'	:	'2_03'
			}
		]
	},
	{
		'id'	:	3,
		'name'	:	'kfc',
		'items' : [
			{
				'name'	:	'mc nugget',
				'price'	:	17.34,
				'id'	:	'3_01'
			},
			{
				'name'	:	'strips small',
				'price'	:	47.34,
				'id'	:	'3_02'
			},
			{
				'name'	:	'bucket',
				'price'	:	99.34,
				'id'	:	'3_03'
			}
		]
	}
]

vendor_data = {
	'1'	: [],
	'2' : [],
	'3' : []
}