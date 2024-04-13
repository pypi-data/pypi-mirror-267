DELIMITER $$

CREATE PROCEDURE `GetTotalCostOfPlan`()
BEGIN
    SELECT
        SUM(c.amount * pp.quantity) AS TotalCostOfPlan
    FROM calculation c
    JOIN production_plan pp ON c.product_id = pp.product_id;
END$$

CREATE PROCEDURE `GetCostItemDetails`()
BEGIN
    SELECT
        ci.name AS CostItem,
        SUM(c.amount * pp.quantity) AS CostItemTotal,
        (SUM(c.amount * pp.quantity) / (SELECT SUM(c2.amount * pp2.quantity) FROM calculation c2 JOIN production_plan pp2 ON c2.product_id = pp2.product_id)) * 100 AS PercentageOfTotalCost
    FROM calculation c
    JOIN cost_items ci ON c.cost_item_id = ci.id
    JOIN production_plan pp ON c.product_id = pp.product_id
    GROUP BY ci.name;
END$$

DELIMITER ;
