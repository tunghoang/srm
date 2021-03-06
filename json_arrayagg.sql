DELIMITER //

DROP FUNCTION IF EXISTS JSON_ARRAYAGG//

CREATE AGGREGATE FUNCTION IF NOT EXISTS JSON_ARRAYAGG(next_value INT) RETURNS TEXT
BEGIN  

 DECLARE json TEXT DEFAULT '[""]';
 DECLARE CONTINUE HANDLER FOR NOT FOUND RETURN json_remove(json, '$[0]');
      LOOP  
          FETCH GROUP NEXT ROW;
          SET json = json_array_append(json, '$', next_value);
      END LOOP;

END //
DELIMITER ;
