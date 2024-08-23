create table fct_cookbook (
	cookbook_id	   bigserial primary key,
	cookbook_name	varchar(250) not null,
	cookbook_desc	varchar(25000),
	creation_date	timestamp,
	created_by		bigint, 
	modified_date 	timestamp, 
	modified_by	    bigint
);


create table cookbook_recipe_map (
	cookbook_id	   bigint,
	recipe_id	   bigint,
	primary key (cookbook_id, recipe_id)
);

create table fct_recipes (
	recipe_id	   bigserial primary key,
	recipe_name	varchar(250) not null,
	recipe_desc	varchar(25000),
	creation_date	timestamp,
	created_by		bigint, 
	modified_date 	timestamp, 
	modified_by	    bigint,
	is_private	 	smallint not null default 1
);

create table fct_recipe_ingredients (
	recipe_ingredient_id	   bigserial primary key,
	recipe_id					bigint	 not null,
	ingredient_id				bigint	 not null,
	quantity					varchar(250),
	unit_of_measure				varchar(250)
);


create table fct_recipe_instructions (
	recipe_instruction_id	   bigserial primary key,
	recipe_id					bigint	 not null,
	instruction					bigint	 not null,
	step_number				integer	 not null
);

create table dim_ingredients (
	ingredient_id	   bigserial primary key,
	ingredient_name	varchar(500) not null,
	ingredient_type	varchar(500),
	creation_date	timestamp
);



-- GET RECIPE INGREDIENTS 
SELECT r.recipe_name
	 , r.recipe_desc
	 , ingr.ingredient_name
	 , ingr.ingredient_type
FROM fct_recipes r
JOIN fct_recipe_ingredients ring
	ON r.recipe_id = ring.recipe_id 
JOIN dim_ingredients ingr
	ON ring.ingredient_id = ingr.ingredient_id ;
	
-- GET RECIPE INSTRUCTIONS
SELECT r.recipe_name
	 , r.recipe_desc
	 , inst.instruction
	 , inst.step_number
FROM fct_recipes r
JOIN fct_recipe_instructions inst
	ON r.recipe_id = inst.recipe_id 
ORDER BY step_number;



create table fct_users (
	user_id	   bigserial primary key,
	username	varchar(250) not null,
	first_name	varchar(250),
	last_name	varchar(250),
	email		varchar(500),
	creation_date	timestamp
);

create table user_cookbook_map (
	user_id		bigint,
	cookbook_id	bigint,
	primary key (user_id, cookbook_id)
);
